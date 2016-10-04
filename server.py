import json
import bottle
import bson
from bottle import route, run
from bson.json_util import dumps
from pymongo import MongoClient
import credentials

client = MongoClient(credentials.databaseUri)
db = client['numberfire-football']
collection = db['players']

# Route to dump of all players

@route('/api', method='GET')
def display_db():
	return dumps(collection.find())

# Route to dump of all players on team

@route('/api/:team', method='GET')
def display_db(team):
	return dumps(collection.find({'team':team}))

# Route to dump of all players of same position

@route('/api/:position', method='GET')
def display_db(position):
	return dumps(collection.find({'position':position}))

run(host='localhost', port=8080)

