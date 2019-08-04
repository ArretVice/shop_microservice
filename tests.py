import requests
import json
from pprint import pprint


test_data = [
    {
            'name': 'iphone',
            'description': 'iphone 4s 32 gb',
            'parameters': {
                'price': 400,
                'color': 'white',
            }
    },
    {
            'name': 'samsung',
            'description': 'samsung 32 gb',
            'parameters': {
                'price': 300,
                'color': 'black',
            }
    },
    {
            'name': 'xiaomi',
            'description': 'xiaomi 32 gb',
            'parameters': {
                'price': 200,
                'color': 'blue',
                'cheap': 'yes',
            }
    }, 
]

stored_id = None

# test inserts
for item in test_data:
    r = requests.post('http://localhost:8080/add', data=json.dumps(item))
    pprint(f'Good request: {r.json()}')
    if not stored_id:
        stored_id = r.json().get('item_id')

# test invalid data insert
r = requests.post('http://localhost:8080/add', data=json.dumps({'name': 'bob', 'age': 42}))
pprint(f'Bad request: {r.json()}')

# test finding by valid ID
r = requests.get('http://localhost:8080/get_info_by_id', data=json.dumps({'id': stored_id}))
print(f'Stored id: {stored_id}')
pprint(f'Found item: {r.json()}')

# test finding by invalid ID
r = requests.get('http://localhost:8080/get_info_by_id', data=json.dumps({'id': '1234abcd1234abcd1234abcd'}))
pprint(f'Error message: {r.json()}')

r = requests.get('http://localhost:8080/get_info_by_id', data=json.dumps({'id': '1234'}))
pprint(f'Error message: {r.json()}')

# test filtering by name
r = requests.get('http://localhost:8080/filter_by', data=json.dumps({'name': 'samsung'}))
pprint(f'Found items by name: {r.json()}')

# test filtering by parameter
r = requests.get('http://localhost:8080/filter_by', data=json.dumps({'parameters': {'price': {'$gt': 200}}}))
pprint(f'Found items: {r.json()}')
