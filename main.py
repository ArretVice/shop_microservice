import asyncio
from bson.objectid import ObjectId

from aiohttp import web
from motor.motor_asyncio import AsyncIOMotorClient


async def setup_db():
    db = AsyncIOMotorClient('localhost', 27017).test
    await db.items.drop()
    return db


async def home(request):
    response_obj = {
        'status': 'success',
        'message': 'homepage',
    }
    return web.json_response(response_obj)


async def add_item(request):
    data = await request.json()
    try:
        name = data['name']
        description = data['description']
        parameters = data['parameters']
        db = request.app['db']
        inserted = await db.items.insert_one(
            {
                'name': name,
                'description': description,
                'parameters': parameters,
            }
        )
        inserted_id = inserted.inserted_id
        response_obj = {
            'status': 'success',
            'message': f'item {name} added to database',
            'item_id': str(inserted_id),
        }
    except Exception as e:
        response_obj = {
            'status': 'failed',
            'message': f'error: {str(e)}',
        }
    return web.json_response(response_obj)


async def get_info_by_id(request):
    data = await request.json()
    try:
        item_id = data['id']
        db = request.app['db']
        if ObjectId.is_valid(item_id):
            found_item = await db.items.find_one({'_id': ObjectId(item_id)})
        else:
            found_item = None
        if found_item:
            item_data = {k: v for (k, v) in found_item.items() if k != '_id'}
            response_obj = {
                'status': 'success',
                'data': item_data,
            }
        else:
            response_obj = {
                'status': 'failed',
                'message': f'error: item with this id {item_id} does not exist'
            }
    except Exception as e:
        response_obj = {
            'status': 'failed',
            'message': f'error: {str(e)}',
        }
    return web.json_response(response_obj)


async def filter_by(request):
    data = await request.json()
    try:
        db = request.app['db']
        name = data.get('name')
        parameters = data.get('parameters')
        items = []
        if name:
            async for item in db.items.find({'name': name}):
                item_data = {k: (v if k != '_id' else str(v)) for (k, v) in item.items()}
                items.append(item_data)
        if parameters:
            for param_key, param_value in parameters.items():
                async for item in db.items.find({f'parameters.{param_key}': param_value}):
                    item_data = {k: (v if k != '_id' else str(v)) for (k, v) in item.items()}
                    items.append(item_data)
        names_list = [filtered_item['name'] for filtered_item in items]
        response_obj = {
                'status': 'success' if items else 'failed',
                'data': names_list if names_list else 'no items found',
        }
    except Exception as e:
        response_obj = {
            'status': 'failed',
            'message': f'error: {str(e)}',
        }
    return web.json_response(response_obj)


loop = asyncio.get_event_loop()
db = loop.run_until_complete(setup_db())
app = web.Application()
app['db'] = db
app.router.add_get('/', home)
app.router.add_post('/add', add_item)
app.router.add_get('/get_info_by_id', get_info_by_id)
app.router.add_get('/filter_by', filter_by)
web.run_app(app, host='127.0.0.1', port=8080)
