from flask import Blueprint, request, jsonify
import pydgraph
import json

dgraph_data = Blueprint('dgraph_data', __name__)

# Dgraph client setup
def create_client():
    client_stub = pydgraph.DgraphClientStub('localhost:9080')
    return pydgraph.DgraphClient(client_stub)

@dgraph_data.route('/dgraph/query', methods=['GET'])
def query_concept():
    concept = request.args.get('concept')
    query = """
    {
        all(func: eq(concept, "%s")) {
            uid
            concept
            explanation
            hashtags {
                uid
                concept
            }
        }
    }
    """ % concept

    client = create_client()
    txn = client.txn()
    try:
        response = txn.query(query)
        response_json = json.loads(response.json)  # Decode the bytes to a string and then to a dictionary
        print(response_json)  # Print the result to verify the data retrieval
        return jsonify(response_json)
    finally:
        txn.discard()
