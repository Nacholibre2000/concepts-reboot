import pydgraph
import os
from dotenv import load_dotenv

load_dotenv()

DGRAPH_HOST = os.getenv('DGRAPH_HOST')
DGRAPH_PORT = os.getenv('DGRAPH_PORT')

def create_dgraph_client():
    client_stub = pydgraph.DgraphClientStub(f'{DGRAPH_HOST}:{DGRAPH_PORT}')
    client = pydgraph.DgraphClient(client_stub)
    return client, client_stub

def export_schema():
    client, client_stub = create_dgraph_client()
    try:
        # Fetch the schema using a query
        query = "schema {}"
        response = client.txn(read_only=True).query(query)
        print(response.json)
    except Exception as e:
        print(f"Error exporting schema: {e}")
    finally:
        client_stub.close()

if __name__ == "__main__":
    export_schema()
