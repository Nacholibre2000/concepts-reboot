from flask import Blueprint, request, jsonify
import pydgraph
import json
from datetime import datetime

node_data = Blueprint('node_data', __name__)

# Dgraph client setup
def create_dgraph_client():
    client_stub = pydgraph.DgraphClientStub('localhost:9080')
    client = pydgraph.DgraphClient(client_stub)
    return client, client_stub

@node_data.route('/node_data/add_node', methods=['POST'])
def add_node():
    data = request.json
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

    # Convert date string to datetime object if it exists
    if date:
        try:
            date = datetime.fromisoformat(date).isoformat()
        except ValueError:
            return jsonify({'message': 'Invalid date format'}), 400

    print(f"Data received: {data}")
    print(f"Formatted date: {date}")

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
            'date': date,  # Ensure date is in ISO format
            'source': source,
            'license': license,
        }

        print(f"Main node: {main_node}")

        # Prepare mutations for hashtags
        hashtag_uids = []
        for tag in hashtags:
            if tag['name']:
                query = None
                if tag['type'] == 'concept':
                    query = f"""
                    {{
                        existingNode as var(func: eq(concept, "{tag['name']}"))
                        query(func: uid(existingNode)) {{
                            uid
                        }}
                    }}
                    """
                elif tag['type'] == 'person':
                    query = f"""
                    {{
                        existingNode as var(func: eq(person, "{tag['name']}"))
                        query(func: uid(existingNode)) {{
                            uid
                        }}
                    }}
                    """
                elif tag['type'] == 'event':
                    query = f"""
                    {{
                        existingNode as var(func: eq(event, "{tag['name']}"))
                        query(func: uid(existingNode)) {{
                            uid
                        }}
                    }}
                    """
                elif tag['type'] == 'place_name':
                    query = f"""
                    {{
                        existingNode as var(func: eq(place_name, "{tag['name']}"))
                        query(func: uid(existingNode)) {{
                            uid
                        }}
                    }}
                    """

                print(f"Query for tag {tag['name']}: {query}")

                if query:
                    response = txn.query(query)
                    result = json.loads(response.json)
                    print(f"Query result for tag {tag['name']}: {result}")
                    if 'query' in result and result['query']:
                        # Use the existing node UID
                        hashtag_uids.append({'uid': result['query'][0]['uid']})
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

        print(f"Hashtag UIDs: {hashtag_uids}")

        # Perform the mutation
        mutations = [txn.create_mutation(set_obj=main_node)]
        for new_tag in hashtag_uids:
            if new_tag['uid'].startswith('_:'):
                mutations.append(txn.create_mutation(set_obj=new_tag))
        txn_request = txn.create_request(mutations=mutations, commit_now=True)
        response = txn.do_request(txn_request)
        
        return jsonify({'message': 'Node added successfully', 'uid': response.uids['newNode']})
    finally:
        txn.discard()
        client_stub.close()
