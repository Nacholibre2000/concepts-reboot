import pydgraph
import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DGRAPH_HOST = os.getenv('DGRAPH_HOST')
DGRAPH_PORT = os.getenv('DGRAPH_PORT')

def create_dgraph_client():
    client_stub = pydgraph.DgraphClientStub(f'{DGRAPH_HOST}:{DGRAPH_PORT}')
    client = pydgraph.DgraphClient(client_stub)
    return client, client_stub

def parse_schema(json_response):
    schema_data = json.loads(json_response)
    schema_parts = []

    # List of predicates to exclude
    exclude_predicates = [
        "dgraph.drop.op",
        "dgraph.graphql.p_query",
        "dgraph.graphql.schema",
        "dgraph.graphql.xid",
        "dgraph.type"
    ]

    for item in schema_data["schema"]:
        predicate = item["predicate"]
        
        # Skip pre-defined Dgraph predicates
        if predicate.startswith("dgraph.") or predicate in exclude_predicates:
            continue

        parts = [f'<{predicate}>: {item["type"]}']
        
        if "index" in item and item["index"]:
            parts.append(f'@index({", ".join(item["tokenizer"])})')
        if item["type"] == "uid":
            # For uid predicates, choose either @reverse or @list, not both
            if "reverse" in item and item["reverse"]:
                parts.append('@reverse')
            elif "list" in item and item["list"]:
                parts.append('@list')
        else:
            # For non-uid predicates, add directives as before
            if "reverse" in item and item["reverse"]:
                parts.append('@reverse')
            if "list" in item and item["list"]:
                parts.append('@list')
        if "upsert" in item and item["upsert"]:
            parts.append('@upsert')
        if "lang" in item and item["lang"]:
            parts.append('@lang')

        schema_parts.append(" ".join(parts) + " .")

    return "\n".join(schema_parts)

    return "\n".join(schema_parts)

def import_schema():
    # Read the JSON response from a file
    with open('dgraph_scripts/schema.json', 'r') as file:
        json_response = file.read()

    schema_str = parse_schema(json_response)

    client, client_stub = create_dgraph_client()
    try:
        # Set the schema
        op = pydgraph.Operation(schema=schema_str)
        print("Schema to be imported:")
        print(schema_str)
        client.alter(op)
        print("Schema imported successfully.")
    except Exception as e:
        print(f"Error importing schema: {e}")
    finally:
        client_stub.close()
