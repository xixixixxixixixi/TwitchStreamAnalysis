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

# get top k rooms
def getTopK(k):
    streams = client.get_streams()  # APICursor containing Stream objects
    streams_top20 = streams._queue  # List of Stream objects
    fields = ['id', 'user_id', 'user_login', 'user_name', 'game_id', 'game_name', 'type', 'title', 'viewer_count',
              'started_at', 'language', 'thumbnail_url', 'tag_ids', 'is_mature']
    data = {'data': []}
    count = 0
    for stream in streams:
        # print(stream)
        d = {}
        for field in fields:
            if field == 'started_at':
                d[field] = stream[field].strftime('%Y-%m-%d %H:%M:%S')
            else:
                d[field] = stream[field]
        data['data'].append(d)
        count += 1
        if count == k - 1:
            break
    return data

# get top k games with viewers
def getTopKGames(k):
    topGames = client.get_top_games()
    print(topGames)
    print(len(topGames))
    gameIds = []
    count = 0
    for game in topGames:
        print(game)
        gameIds.append(game['id'])
        count += 1
        if count == k:
            break
    print(gameIds)
    streams = client.get_streams(game_ids=gameIds,page_size=100)
    print(streams)
    count = 0
    gameDict = {}
    for stream in streams:
        # print(stream)
        if gameDict.__contains__(stream['game_name']):
            gameDict[stream['game_name']] += stream['viewer_count']
        else:
            gameDict[stream['game_name']] = stream['viewer_count']
        print(gameDict)
        count += 1
        if count == 5000:
            break
    result = []
    gameDictTuple = sorted(gameDict.items(), key=lambda d: d[1], reverse=True)
    for game in gameDictTuple:
        result.append({
            "gameName": game[0],
            "peopleNum": game[1]
        })
    return result

# get viewers for a specific room
def getViewerTrendForOneRoom(id):
    streams = client.get_streams(user_ids = [str(id)])
    return streams[0]['viewer_count']

# #%%
# def stream_preprocess(streams):
#     """
#
#     :param streams: list of Stream objects
#     :return:
#     {'data': [{'id': ***, 'user_id': ***, 'user_login': ***, 'user_name': ***, ..., 'tag_ids': ***, 'is_mature': ***},
#               {'id': ***, 'user_id': ***, 'user_login': ***, 'user_name': ***, ..., 'tag_ids': ***, 'is_mature': ***},
#               ...
#               ]
#     }
#     """
#
#     fields = ['id', 'user_id', 'user_login', 'user_name', 'game_id', 'game_name', 'type', 'title', 'viewer_count',
#               'started_at', 'language', 'thumbnail_url', 'tag_ids', 'is_mature']
#     data = {'data': []}
#     for stream in streams:
#         print(stream)
#         d = {}
#         for field in fields:
#             if field == 'started_at':
#                 d[field] = stream[field].strftime('%Y-%m-%d %H:%M:%S')
#             else:
#                 d[field] = stream[field]
#         data['data'].append(d)
#
#     return data

