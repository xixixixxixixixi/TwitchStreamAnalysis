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


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/topK/<num>', methods=['GET'])
def topK(num):  # put application's code here
    if request.method == 'GET':
        num = int(num)
        data = TwitchHTTPClient.getTopK(num)
        print(data)
        # data = {'data':
        #             [
        #                 {'id': '40230484139', 'user_id': '83232866', 'user_login': 'ibai', 'user_name': 'ibai',
        #                  'game_id': '518203', 'game_name': 'Sports', 'type': 'live', 'title': 'PADEL DE LAS ESTRELLAS 2 | EL TORNEO DE PADEL DEL AÑO ',
        #                  'viewer_count': 112452, 'started_at': '2021-11-18 18:13:47', 'language': 'es',
        #                  'thumbnail_url': 'https://static-cdn.jtvnw.net/previews-ttv/live_user_ibai-{width}x{height}.jpg',
        #                  'tag_ids': ['d4bb9c58-2141-4881-bcdc-3fe0505457d1'], 'is_mature': False}
        #             ]
        # }
        result = {}
        roomList = data['data']
        gameList = GetGraph.gameAndViewerGraph(roomList)
        result['gameAndViewerGraph'] = gameList
        return json.dumps(result)

@app.route('/topKGames/<num>', methods=['GET'])
def topKGames(num):  # put application's code here
    if request.method == 'GET':
        num = int(num)
        data = TwitchHTTPClient.getTopKGames(num)
        result = {}
        result['gameAndViewerGraph'] = data
        return json.dumps(result)

@app.route('/trend/<userId>')
def trend(userId):  # put application's code here
    num = int(userId)
    data = TwitchHTTPClient.getViewerTrendForOneRoom(userId)
    return json.dumps(data)


if __name__ == '__main__':
    app.run()
