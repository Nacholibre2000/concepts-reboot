from flask import Blueprint, request, jsonify
import pydgraph
import json

dgraph_data = Blueprint('dgraph_data', __name__)

# Dgraph client setup
def create_dgraph_client():
    client_stub = pydgraph.DgraphClientStub('localhost:9080')
    client = pydgraph.DgraphClient(client_stub)
    return client, client_stub

@dgraph_data.route('/add_node', methods=['POST'])
def add_node():
    data = request.json
    image_url = data.get('image_url')
    concept = data.get('name')
    person = data.get('person')
    event = data.get('event')
    place_name = data.get('place_name')
    explanation = data.get('explanation')
    place_geo = data.get('place_geo')  # Assuming this is GeoJSON format
    date = data.get('date')
    source = data.get('source')
    license = data.get('license')

    client, client_stub = create_dgraph_client()
    txn = client.txn()

    try:
        p = {
            'uid': '_:newNode',
            'image_url': image_url,
            'concept': concept,
            'person': person,
            'event': event,
            'place_name': place_name,
            'explanation': explanation,
            'place_geo': place_geo,
            'date': date,
            'source': source,
            'license': license,
        }
        mutation = txn.create_mutation(set_obj=p)
        request = txn.create_request(mutations=[mutation], commit_now=True)
        response = txn.do_request(request)
        txn.commit()

        return jsonify({'message': 'Node added successfully', 'uid': response.uids['newNode']})
    except Exception as e:
        return jsonify({'message': 'Failed to add node', 'error': str(e)}), 500
    finally:
        txn.discard()
        client_stub.close()

@dgraph_data.route('/dgraph/query', methods=['GET'])
def query_node():
    node_value = request.args.get('node')
    
    # Define the possible predicates to search for
    predicates = ["concept", "person", "event", "place_name"]

    # Construct the query with unique aliases
    query_parts = []
    for i, predicate in enumerate(predicates):
        query_parts.append(f'query{i} as var(func: eq({predicate}, "{node_value}"))')

    query = f"""
    {{
        { " ".join(query_parts) }
        results(func: uid(query0, query1, query2, query3)) {{
            uid
            concept
            person
            event
            place_name
            explanation
            place_
            image_url
            date
            source
            license
            hashtags {{
                uid
                concept
                person
                event
                place_name
            }}
        }}
    }}
    """

    client, client_stub = create_dgraph_client()
    txn = client.txn()
    try:
        response = txn.query(query)
        response_json = json.loads(response.json)
        print(response_json)  # Print the result to verify the data retrieval
        return jsonify(response_json)
    finally:
        txn.discard()
        client_stub.close()

