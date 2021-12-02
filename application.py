import json

from flask import Flask
from flask import *
from flask_cors import CORS
import twitch
from ApiInterface import TwitchHTTPClient
# Credentials

application = Flask(__name__)
CORS(application, support_credentials = True)

# bk
@application.route('/')
def hello_world():  # put application's code here
    return render_template("index.html")

@application.route('/topKGames/<num>', methods=['GET'])
def topKGames(num):  # put application's code here
    if request.method == 'GET':
        data = TwitchHTTPClient.getTopKGames(int(num))
        return json.dumps(data)

@application.route('/topKTags/<num>', methods=['GET'])
def topKTags(num):  # put application's code here
    if request.method == 'GET':
        data = TwitchHTTPClient.getTopKTags(int(num))
        return json.dumps(data)

@application.route('/getLanguageCount/<num>', methods=['GET'])
def getLanguageCount(num):  # put application's code here
    if request.method == 'GET':
        result = TwitchHTTPClient.getLanguageForRooms(int(num))
        return json.dumps(result)

@application.route('/getChannelStreamSchedule/<num>', methods=['GET'])
def getChannelStreamSchedule(num):  # put application's code here
    if request.method == 'GET':
        result = TwitchHTTPClient.getChannelStreamSchedule(int(num))
        return json.dumps(result)



# @app.route('/trend/<userId>')
# def trend(userId):  # put application's code here
#     num = int(userId)
#     data = TwitchHTTPClient.getViewerTrendForOneRoom(userId)
#     return json.dumps(data)


if __name__ == '__main__':
    application.run()
