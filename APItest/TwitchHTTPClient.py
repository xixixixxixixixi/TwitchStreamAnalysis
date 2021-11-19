#%%
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Columbia EECS E6893 Big Data Analytics

"""
This module is used to pull data from twitch API and preprocess the data

"""

import twitch

# Credentials
client_id = '918pxgmrcct2dbuwu7tih5na23ogxq'
oauth_token = 'if6rhr2bfebpxqlie36i66bazekgz0'

client = twitch.TwitchHelix(client_id=client_id, oauth_token=oauth_token)
# streams = client.get_streams()  # APICursor containing Stream objects
# streams_top20 = streams._queue  # List of Stream objects

# get top k games with viewers
'''
    function: get top k popular game and return game name with correspoding viewers
    
    data format for result: 
    ['game1', 'viewers'],
    ['game2', 43.3, 85.8, 93.7],
    ['game3', 83.1, 73.4, 55.1],
    ['game4', 86.4, 65.2, 82.5],
    ['game5', 72.4, 53.9, 39.1]
'''
def getTopKGames(k):
    topGames = client.get_top_games()
    gameIds = []
    count = 0
    for game in topGames:
        gameIds.append(game['id'])
        count += 1
        if count == k:
            break
    streams = client.get_streams(game_ids=gameIds,page_size=100)
    count = 0
    gameDict = {}
    for stream in streams:
        if gameDict.__contains__(stream['game_name']):
            gameDict[stream['game_name']] += stream['viewer_count']
        else:
            gameDict[stream['game_name']] = stream['viewer_count']
        print(gameDict)
        count += 1
        if count == 5000:
            break
    result = []
    result.append(['game', 'viewers'])
    for game in sorted(gameDict.items(), key=lambda d: d[1], reverse=True):
        result.append([game[0], game[1]])
    return result

# get viewers for a specific room
def getViewerTrendForOneRoom(id):
    streams = client.get_streams(user_ids = [str(id)])
    return streams[0]['viewer_count']


