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
CORS(app, support_credentials=True)


@app.route('/')
def hello_world():  # put application's code here
    return render_template("index.html")


@app.route('/renderPredictionPage')
def predictionPage():  # put application's code here
    return render_template("prediction.html")


@app.route('/renderClipSearch')
def clipSearchPage():  # put application's code here
    return render_template("searchClips.html")


@app.route('/renderfurtherGameAnalysis')
def furtherGameAnalysisPage():  # put application's code here
    return render_template("furtherGameAnalysis.html")


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


@app.route('/getDailyMeanViewerCount', methods=['GET'])
def getMeanViewerCount():  # put application's code here
    if request.method == 'GET':
        result = TwitchHTTPClient.getDailyMeanViewerCount()
        return json.dumps(result)


@app.route('/getDynamicPopularGamesBarChart', methods=['POST'])
def getDynamicPopularGamesBarChart():  # put application's code here
    if request.method == 'POST':
        game_list = request.data
        print(game_list)
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        result = TwitchHTTPClient.getDynamicHistory(game_list)
        return json.dumps(result)


@app.route('/getViewerPrediction', methods=['POST'])
def getViewerPrediction():  # put application's code here
    if request.method == 'POST':
        game_name = request.data
        print(game_name)
        result = TwitchHTTPClient.getPrediction(game_name.decode())
        return json.dumps(result)


@app.route('/getClipsByUser', methods=['POST'])
def getClipsByUser():  # put application's code here
    if request.method == 'POST':
        user_name = request.data
        print(user_name)
        result = TwitchHTTPClient.getClipsByUserRequest(user_name.decode())
        print(result)
        return json.dumps(result)


@app.route('/wordCloudForGamesViewer/<num>', methods=['GET'])
def wordCloudForGamesViewer(num):  # put application's code here
    if request.method == 'GET':
        result = TwitchHTTPClient.getWordCloudDataForTopGamesViewerCount(num)
        print(result)
        return json.dumps(result)


if __name__ == '__main__':
    app.run()
