import json

from flask import Flask
from flask import *
from flask_cors import CORS
import twitch
from APItest import TwitchHTTPClient
import GetGraph
# Credentials

app = Flask(__name__)
CORS(app, support_credentials = True)

# 
@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/topKGames/<num>', methods=['GET'])
def topKGames(num):  # put application's code here
    if request.method == 'GET':
        num = int(num)
        data = TwitchHTTPClient.getTopKGames(num)
        return json.dumps(data)

@app.route('/topKTags/<num>', methods=['GET'])
def topKTags(num):  # put application's code here
    if request.method == 'GET':
        num = int(num)
        data = TwitchHTTPClient.getTopKTags(num)
        return json.dumps(data)

@app.route('/getLanguageCount/<num>', methods=['GET'])
def getLanguageCount(num):  # put application's code here
    if request.method == 'GET':
        num = int(num)
        result = TwitchHTTPClient.getLanguageForRooms(num)
        return json.dumps(result)



# @app.route('/trend/<userId>')
# def trend(userId):  # put application's code here
#     num = int(userId)
#     data = TwitchHTTPClient.getViewerTrendForOneRoom(userId)
#     return json.dumps(data)


if __name__ == '__main__':
    app.run()
