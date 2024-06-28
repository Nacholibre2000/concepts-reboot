import os
import json
import psycopg2
import pydgraph
import logging
from urllib.parse import urlparse
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.DEBUG, filename='import_log.log', filemode='w')
logger = logging.getLogger(__name__)

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
            data.append({"id": str(row[0]), "table": table})  # Convert id to string

    logger.debug(f"Fetched {len(data)} items from PostgreSQL:")
    for item in data:
        logger.debug(item)

    client, client_stub = create_dgraph_client()

    try:
        for item in data:
            logger.debug(item)
            curriculum_composite_key = f"{item['table']}_{item['id']}"
            query = f"""
            {{
                existing_node(func: eq(curriculum_composite_key, "{curriculum_composite_key}")) {{
                    uid
                    id
                    curriculum_table
                    composite_key
                    hashtags
                }}
            }}
            """
            logger.debug(f"Query to check existing node: {query}")
            
            # Use a new transaction for each query
            txn = client.txn()
            try:
                response = txn.query(query)
                response_json = response.json.decode('utf-8')
                logger.debug(f"Response JSON: {response_json}")
                existing_nodes = json.loads(response_json).get('existing_node', [])
            finally:
                txn.discard()

            if existing_nodes:
                uid = existing_nodes[0]['uid']
                logger.debug(f"Updating existing node with uid: {uid}")
                # Ensure hashtags is added to existing nodes
                node = {
                    "uid": uid,
                    "hashtags": []
                }
            else:
                uid = "_:newNode"
                logger.debug("No nodes found. Creating new node.")

            node = {
                "uid": uid,
                "id": str(item["id"]),
                "curriculum_table": item["table"],
                "curriculum_composite_key": curriculum_composite_key,
                "hashtags": []
            }
            logger.debug(f"set_json: {node}")
            
            # Immediately upsert this node
            mutation = pydgraph.Mutation(set_json=json.dumps(node).encode('utf-8'))
            txn = client.txn()
            try:
                response = txn.mutate(mutation)
                txn.commit()
                logger.debug(f"Upserted node: {response.uids}")
            except Exception as e:
                logger.error(f"Error upserting node: {e}")
            finally:
                txn.discard()

        logger.info("Data successfully imported into Dgraph.")

    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        client_stub.close()
        conn.close()

if __name__ == "__main__":
    import_data_to_dgraph()