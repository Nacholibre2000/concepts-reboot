from flask import Blueprint, request, jsonify, make_response
import pydgraph
import json


node_data = Blueprint('node_data', __name__)

# Dgraph client setup
def create_dgraph_client():
    client_stub = pydgraph.DgraphClientStub('localhost:9080')
    client = pydgraph.DgraphClient(client_stub)
    return client, client_stub

@node_data.route('/node_data/add_node', methods=['POST', 'OPTIONS'])
def add_node():
    if request.method == 'OPTIONS':
        return _build_cors_preflight_response()
    
    # Print request headers
    print("Request Headers:", request.headers)
    
    # Verify if content-type is application/json
    if request.content_type != 'application/json':
        print("Content-Type is not application/json")
        return jsonify({'message': 'Content-Type must be application/json'}), 400

    # Print the raw data received
    raw_data = request.get_data()
    print("Raw Data Received:", raw_data)

    try:
        # Try to parse JSON data
        data = request.get_json()  # Ensure we get the JSON data correctly
        if data is None:
            print("No JSON data received")
            return jsonify({'message': 'No JSON data received'}), 400

        print(f"Received data: {data}")  # Print the received JSON data

        image_url = data.get('image_url')
        concept = data.get('concept')
        person = data.get('person')
        event = data.get('event')
        place_name = data.get('place_name')
        explanation = data.get('explanation')
        place_geo = data.get('place_geo')  # Assuming this is GeoJSON format
        date = data.get('date')
        source = data.get('source')
        license = data.get('license')
        hashtags = data.get('hashtags', [])  # List of hashtag objects

        client, client_stub = create_dgraph_client()
        txn = client.txn()

        try:
            # Prepare the main node
            main_node = {
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

            # Prepare mutations for hashtags
            hashtag_uids = []
            for tag in hashtags:
                query = None
                if tag['type'] == 'concept':
                    query = """
                    {
                        existingNode as var(func: eq(concept, "%s"))
                    }
                    """ % tag['name']
                elif tag['type'] == 'person':
                    query = """
                    {
                        existingNode as var(func: eq(person, "%s"))
                    }
                    """ % tag['name']
                elif tag['type'] == 'event':
                    query = """
                    {
                        existingNode as var(func: eq(event, "%s"))
                    }
                    """ % tag['name']
                elif tag['type'] == 'place_name':
                    query = """
                    {
                        existingNode as var(func: eq(place_name, "%s"))
                    }
                    """ % tag['name']

                if query:
                    response = txn.query(query)
                    result = json.loads(response.json)
                    if result['existingNode']:
                        # Use the existing node UID
                        hashtag_uids.append({'uid': result['existingNode'][0]['uid']})
                    else:
                        # Create a new node
                        new_tag = {
                            'uid': f'_:newTag{len(hashtag_uids)}',  # Create unique blank node identifier
                            tag['type']: tag['name']
                        }
                        hashtag_uids.append(new_tag)

            # Link hashtags to the main node
            if hashtag_uids:
                main_node['hashtags'] = hashtag_uids

            # Perform the mutation
            mutations = [txn.create_mutation(set_obj=main_node)]
            for new_tag in hashtag_uids:
                if new_tag['uid'].startswith('_:'):
                    mutations.append(txn.create_mutation(set_obj=new_tag))

            request = txn.create_request(mutations=mutations, commit_now=True)
            response = txn.do_request(request)
            txn.commit()

            return _corsify_actual_response(jsonify({'message': 'Node added successfully', 'uid': response.uids['newNode']}))
        except Exception as e:
            return _corsify_actual_response(jsonify({'message': 'Failed to add node', 'error': str(e)}), 500)
        finally:
            txn.discard()
            client_stub.close()
    except Exception as e:
        print(f"Error occurred: {e}")
        return _corsify_actual_response(jsonify({'message': 'Failed to add node', 'error': str(e)}), 500)

@node_data.route('/node_data/query', methods=['GET'])
def query_node():
    node_value = request.args.get('node')
    
    if not node_value:
        return jsonify({"message": "Missing query parameter: node"}), 400
    
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
            place_geo
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

def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "http://localhost:5173")
    response.headers.add('Access-Control-Allow-Headers', "Content-Type,Authorization")
    response.headers.add('Access-Control-Allow-Methods', "GET,PUT,POST,DELETE,OPTIONS")
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "http://localhost:5173")
    response.headers.add('Access-Control-Allow-Headers', "Content-Type,Authorization")
    response.headers.add('Access-Control-Allow-Methods', "GET,PUT,POST,DELETE,OPTIONS")
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response
