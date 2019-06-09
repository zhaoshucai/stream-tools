import json

from bson import ObjectId
from flask import Flask, jsonify, request
# from flask_restful import Resource, Api
from flask_pymongo import PyMongo

app = Flask(__name__)
# api = Api(app)

app.config['MONGO_DBNAME'] = 'freeiptv'

app.config['MONGO_URI'] = 'mongodb://localhost:27070/freeiptv'

app.config.update(
    MONGO_HOST='localhost',
    MONGO_PORT=27017,
    MONGO_USERNAME='',
    MONGO_PASSWORD='',
    MONGO_DBNAME='freeiptv'
)

mongo = PyMongo(app)


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)



@app.route('/playitems')
def playitems():

    channel = request.args.get('channel')
    keyword = request.args.get('keyword')

    query = []
    if channel:
        channel_query = {"channel": {"$eq": channel}}
        query.append(channel_query)
    if keyword:
        keyword_query = {"tags": {"$elemMatch": {"$regex": ".*{}.*".format(keyword), "$options": "i"}}}
        query.append(keyword_query)

    if len(query) > 0:
        result = mongo.db.playitems.find({"$and": query})
    else:
        result = mongo.db.playitems.find()

    output = []
    for s in result:
        output.append(s)

    return JSONEncoder().encode(output)


@app.route('/channels')
def channels():

    channel = request.args.get('channel')
    keyword = request.args.get('keyword')
    type = request.args.get('type')

    query = []
    if channel:
        channel_query = {"_id": {"$eq": channel}}
        query.append(channel_query)
    if keyword:
        keyword_query = {"name": {"$regex": ".*{}.*".format(keyword), "$options": "i"}}
        query.append(keyword_query)
    if type:
        type_query = {"type": {"$eq": type}}
        query.append(type_query)

    result = []
    if len(query) > 0:
        result = mongo.db.channels.find({"$and": query})

    else:
        result = mongo.db.channels.find()

    output = []
    for s in result:
        output.append(s)

    return JSONEncoder().encode(output)


if __name__ == '__main__':
    app.debug = True
    app.run()