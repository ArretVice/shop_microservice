# Shop microservice

This microservice allows you to create items, store them in the database, find items by their ID and filter by parameter.

## Installation

### 1. Clone the repo
```sh
$ git clone git@github.com:ArretVice/shop_microservice.git
$ cd shop_microservice/
```

### 2. Create virtual environment
```sh
$ virtualenv env
$ source env/bin/activate
```

### 3. Install dependencies
```sh
$ pip install -r requirements.txt
```

### 4. Install Docker
Follow these instructions: [here](https://docs.docker.com/install/linux/docker-ce/ubuntu/#prerequisites "here")

### 5. Run database in a docker container
```sh
$ sudo docker run -d -p 27017:27017 mongo
```
Check [localhost:27017](http://localhost:27017 "localhost:27017") in your browser, you should get response: "It looks like you are trying to access MongoDB over HTTP on the native driver port."

### 5. Run server
```sh
$ python main.py
```
Check [localhost:8080](http://localhost:8080 "localhost:8080") in your browser, you should get response: "{"status": "success", "message": "homepage"}"

## Installation complete!


## Test scenario:

#### 1.1. Create item:
```sh
$ curl -X POST http://localhost:8080/add \
-H "Content-Type: application/json" \
-d '{"name":"iphone", "description":"iphone 4s 32 gb", "parameters":{"price":400, "color":"white"}}'
```
You should get response with status:success and item's ID

or

#### 1.2. Create item and save its ID to file:
```sh
$ curl -X POST http://localhost:8080/add \
-H "Content-Type: application/json" \
-d '{"name":"iphone", "description":"iphone 4s 32 gb", "parameters":{"price":400, "color":"white"}}' \
| python3 -c "import sys, json; print(json.load(sys.stdin)['item_id'])" > 'created_item.txt'
```
Item's ID located in file "created_item.txt". This ID will be used fro testing later.

#### 2. Find item by parameter:
```sh
$ curl -X GET "http://localhost:8080/filter_by" \
-H 'Content-Type: application/json' \
-d '{"parameters":{"price":400}}'
```
You will get response with a list of items according to specified parameter.

#### 3. Find item by parameter:
```sh
$ curl -X GET "http://localhost:8080/get_info_by_id" \
-H 'Content-Type: application/json' \
-d '{"id":"<<item ID>>"}'
```
Replace <<item ID>> with desired item's ID, which would be conveniently saved in a file "created_item.txt", if you decided to go with step 1.2.

You will get response with full information about stored item.


## Extras:
You may wish to populate database with some items and test few things.
Do this with:
```sh
$ python tests.py
```
This is not a dedicated test module, but gets the job done.

Also you may check the items stored in the database, do this with:
```sh
$ python check_db.py
```
Remember that every time you restart server, the database will be dropped.
