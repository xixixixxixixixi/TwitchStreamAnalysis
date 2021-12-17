import json
import flask
from flask import Flask
from flask import *
from flask_cors import CORS
import twitch
from ApiInterface import TwitchHTTPClient
# Credentials
# build: https://stackabuse.com/deploying-a-flask-application-to-heroku/
app = Flask(__name__)
CORS(app, support_credentials = True)


@app.route('/')
def hello_world():  # put application's code here
    return render_template("index.html")


@app.route('/topKGames/<num>', methods=['GET'])
def topKGames(num):  # put application's code here
    if request.method == 'GET':
        data = TwitchHTTPClient.getTopKGames(int(num))
        return json.dumps(data)


@app.route('/topKTags/<num>', methods=['GET'])
def topKTags(num):  # put application's code here
    if request.method == 'GET':
        data = TwitchHTTPClient.getTopKTags(int(num))
        return json.dumps(data)


@app.route('/getLanguageCount/<num>', methods=['GET'])
def getLanguageCount(num):  # put application's code here
    if request.method == 'GET':
        result = TwitchHTTPClient.getLanguageForRooms(int(num))
        return json.dumps(result)


@app.route('/getChannelStreamSchedule/<num>', methods=['GET'])
def getChannelStreamSchedule(num):  # put application's code here
    if request.method == 'GET':
        result = TwitchHTTPClient.getChannelStreamSchedule(int(num))
        return json.dumps(result)


@app.route('/getDynamicPopularGamesBarChart', methods=['POST'])
def getDynamicPopularGamesBarChart():  # put application's code here
    if request.method == 'POST':
        game_list = request.data
        print(game_list)
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        result = TwitchHTTPClient.getDynamicHistory(game_list.decode())
        return json.dumps(result)


@app.route('/renderPredictionPage')
def predictionPage():  # put application's code here
    return render_template("prediction.html")


@app.route('/getViewerPrediction', methods=['POST'])
def getViewerPrediction():  # put application's code here
    if request.method == 'POST':
        game_name = request.data
        print(game_name)
        result = TwitchHTTPClient.getPrediction(game_name.decode())
        return json.dumps(result)


if __name__ == '__main__':
    app.run()
