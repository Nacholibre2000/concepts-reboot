import pydgraph
from dotenv import load_dotenv
import os

load_dotenv()

# Dgraph connection details from environment variables
DGRAPH_HOST = os.getenv('DGRAPH_HOST')
DGRAPH_PORT = os.getenv('DGRAPH_PORT')

def create_dgraph_client():
    client_stub = pydgraph.DgraphClientStub(f'{DGRAPH_HOST}:{DGRAPH_PORT}')
    client = pydgraph.DgraphClient(client_stub)
    return client, client_stub

def drop_all_data():
    client, client_stub = create_dgraph_client()
    try:
        op = pydgraph.Operation(drop_all=True)
        client.alter(op)
        print("All data dropped from Dgraph.")
    except Exception as e:
        print(f"Error dropping data: {e}")
    finally:
        client_stub.close()

if __name__ == "__main__":
    drop_all_data()