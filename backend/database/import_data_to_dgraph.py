import os
import psycopg2
import pydgraph
import logging
from dotenv import load_dotenv
from urllib.parse import urlparse
import json

# Set up logging
logging.basicConfig(filename='import_log.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')

# Load environment variables from .env file
load_dotenv()

# Parse PostgreSQL connection details from DATABASE_URL
DATABASE_URL = os.getenv('DATABASE_URL')
url = urlparse(DATABASE_URL)

PG_DBNAME = url.path[1:]  # Remove the leading '/'
PG_USER = url.username
PG_PASSWORD = url.password
PG_HOST = url.hostname
PG_PORT = url.port

# Dgraph connection details from environment variables
DGRAPH_HOST = os.getenv('DGRAPH_HOST')
DGRAPH_PORT = os.getenv('DGRAPH_PORT')

# Function to create PostgreSQL connection
def create_pg_connection():
    conn = psycopg2.connect(
        dbname=PG_DBNAME,
        user=PG_USER,
        password=PG_PASSWORD,
        host=PG_HOST,
        port=PG_PORT
    )
    return conn

# Function to create Dgraph client
def create_dgraph_client():
    client_stub = pydgraph.DgraphClientStub(f'{DGRAPH_HOST}:{DGRAPH_PORT}')
    client = pydgraph.DgraphClient(client_stub)
    return client, client_stub

# Function to check if node exists in Dgraph
def check_node_exists(client, node_id, table):
    query = f"""
    {{
      node_exists(func: eq(id, "{node_id}")) @filter(eq(curriculum_table, "{table}")) {{
        uid
      }}
    }}
    """
    response = client.txn(read_only=True).query(query)
    result = json.loads(response.json)
    print(result)
    if "node_exists" in result and len(result["node_exists"]) > 0:
        return result["node_exists"][0]["uid"]
    return None

# Main function to perform the database operations
def import_data_to_dgraph():
    conn = create_pg_connection()
    cur = conn.cursor()

    tables = ["central_contents", "central_requirements"]
    data = []

    for table in tables:
        cur.execute(f"SELECT id FROM {table}")
        rows = cur.fetchall()
        for row in rows:
            data.append({"id": row[0], "table": table})

    # Log the data fetched from PostgreSQL
    logging.debug(f"Fetched {len(data)} items from PostgreSQL:")
    for item in data:
        logging.debug(item)

    client, client_stub = create_dgraph_client()
    txn = client.txn()

    try:
        mutations = []
        for item in data:
            node_uid = check_node_exists(client, item["id"], item["table"])
            if node_uid:
                # Update existing node
                node = {
                    "uid": node_uid,
                    "id": str(item["id"]),  # Ensure id is a string
                    "curriculum_table": str(item["table"])  # Ensure table is a string
                }
            else:
                # Create new node
                node = {
                    "uid": "_:newNode",
                    "id": str(item["id"]),  # Ensure id is a string
                    "curriculum_table": str(item["table"])  # Ensure table is a string
                }

            # Log the node being processed
            logging.debug(f"Processing node: {node}")
            # Check if node can be encoded correctly
            try:
                json_data = json.dumps(node)
                json_data.encode('utf-8')
            except UnicodeEncodeError as e:
                logging.error(f"Encoding error for node: {node} - {e}")
                continue

            mutations.append(pydgraph.Mutation(set_json=json_data.encode('utf-8')))

        # Log the mutations to be sent to Dgraph
        logging.debug(f"Preparing {len(mutations)} mutations for Dgraph:")
        for mutation in mutations:
            logging.debug(mutation)

        req = pydgraph.Request(mutations=mutations, commit_now=True)
        txn.do_request(req)
        logging.info("Data successfully imported into Dgraph.")

    except Exception as e:
        logging.error(f"An error occurred: {e}")
    
    finally:
        txn.discard()
        client_stub.close()
        conn.close()

if __name__ == "__main__":
    import_data_to_dgraph()
