from flask_restful import Resource, Api, reqparse
from flask import Flask, jsonify, render_template, request
from flask_pymongo import PyMongo
import json

from bson.json_util import dumps

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://heroku_sgnt6qng:3b864au43jrrv6dqllicsi3mvk@ds261296.mlab.com:61296/heroku_sgnt6qng'

mongo = PyMongo(app)
api = Api(app)
parser = reqparse.RequestParser()



class AllProfile(Resource):
    def get(self):
        try:
            query = {}
            projection = {'_id':False}
            scoreSportData = mongo.db.name_surname.find(query, projection)
            listData = []
            for element in scoreSportData:
                listData.append(element)
            return jsonify(listData)
        except:
            return 'Not found'

api.add_resource(AllProfile, '/')



if __name__ == '__main__':
    app.run(debug=True)