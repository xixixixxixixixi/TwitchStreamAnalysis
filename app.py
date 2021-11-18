import json

from flask import Flask
import twitch
from APItest import TwitchHTTPClient
# Credentials

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/topK/<num>')
def topK(num):  # put application's code here
    data = TwitchHTTPClient.getTopK(num)
    return json.dumps(data)

# GET 127.0.0.1:5000/topK/50


if __name__ == '__main__':
    app.run()
