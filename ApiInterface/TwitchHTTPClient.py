#%%
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Columbia EECS E6893 Big Data Analytics
import datetime as dt
"""
This module is used to pull data from twitch API and preprocess the data

"""

import twitch
import requests
import json
import datetime

# Credentials
client_id = '918pxgmrcct2dbuwu7tih5na23ogxq'
oauth_token = '1i4yw3bxxn7csdi3k690hi9q87g6eq'

client = twitch.TwitchHelix(client_id=client_id, oauth_token=oauth_token)
# streams = client.get_streams()  # APICursor containing Stream objects
# streams_top20 = streams._queue  # List of Stream objects

# get top k games with viewers
'''
    function: get top k popular game and return game name with correspoding viewers
    (test with 5000 most popular rooms)
    
    data format for result: 
    ['game', 'viewers'],
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


'''
    function: get top k popular tags(test with 100 most popular rooms)

    data format for result: 
    ['tag', 'count'],
    ['tag1', 3],
    ['tag2', 3],
    ['tag3', 2],
    ['tag4', 1]
'''
def getTopKTags(k):
    streams = client.get_streams(page_size=100)
    count = 0
    result = []
    tagDict = {}
    for stream in streams:
        headers = {
            # 'content-type': 'application/json',
            'Authorization': 'Bearer ' + oauth_token,
            'Client-Id': client_id
        }
        url = 'https://api.twitch.tv/helix/streams/tags' + '?' + 'broadcaster_id=' + stream['user_id']
        response = json.loads(requests.get(url, headers=headers).content.decode('utf-8'))
        # print(response)
        # print(len(response['data']))
        # TODO: finish key error check
        for tag in response['data']:
            if tagDict.__contains__(tag['tag_id']):
                tagDict[tag['tag_id']][1] += 1
            else:
                tagDict[tag['tag_id']] = [tag['localization_names']['en-us'], 1]
        print(tagDict)
        count += 1
        if count == 100:
            break
    result = []
    result.append(['tag', 'count'])
    count = 0
    for tag in sorted(tagDict.items(), key=lambda d: d[1][1], reverse=True):
        result.append([tag[1][0], tag[1][1]])
        count += 1
        if count == k:
            break
    print(result)
    # for language in sorted(languageDict.items(), key=lambda d: d[1], reverse=True):
    #     result.append({'value': language[1], 'name': language[0]})
    return result
    # https://www.cnblogs.com/skzxc/p/12688423.html



'''
    function: get language counts for top k rooms

    data format for result: 
    [
        {'name': 'en', 'value': 1},
        {'name': 'cn', 'value': 2}
    ]
'''
def getLanguageForRooms(k):
    streams = client.get_streams(page_size=100)
    count = 0
    result = []
    languageDict = {}
    for stream in streams:
        print(stream)
        if languageDict.__contains__(stream['language']):
            languageDict[stream['language']] += 1
        else:
            languageDict[stream['language']] = 1
        count += 1
        if count == k:
            break
    for language in sorted(languageDict.items(), key=lambda d: d[1], reverse=True):
        result.append({'value': language[1], 'name': language[0]})
    return result


# # get top m chips with viewers for top k games
# '''
#     function: get top m chips with viewers for top k games
#     documentation: https://dev.twitch.tv/docs/api/reference#get-clips
#
#     data format for result:
#     ['clip', 'viewers'],
#     ['clip1', 123],
#     ['clip2', 456]
# '''
# def getTopKClips(m, k):
#     topGames = client.get_top_games()
#     gameIds = []
#     count = 0
#     for game in topGames:
#         gameIds.append(game['id'])
#         count += 1
#         if count == k:
#             break
#     topKClipsDict = {}
#     for gameId in gameIds:
#         headers = {
#             # 'content-type': 'application/json',
#             'Authorization': 'Bearer ' + oauth_token,
#             'Client-Id': client_id
#         }
#         url = 'https://api.twitch.tv/helix/clips' + '?' + 'game_id=' + gameId
#         response = json.loads(requests.get(url, headers=headers).content.decode('utf-8'))
#         for clip in response['data']:
#
#         print(response)
#
# getTopKClips(4,4)

def getChannelStreamSchedule(k):
    streams = client.get_streams(page_size=100)
    count = 0
    scheduleDict = {}
    scheduleDict['name'] = []
    scheduleDict['starttime'] = []
    scheduleDict['endtime'] = []
    scheduleDict['duration'] = []
    for stream in streams:
        userId = stream['user_id']
        headers = {
            'Authorization': 'Bearer ' + oauth_token,
            'Client-Id': client_id
        }
        url = 'https://api.twitch.tv/helix/schedule' + '?' + 'broadcaster_id=' + userId
        response = json.loads(requests.get(url, headers=headers).content.decode('utf-8'))
        # print(response)
        if not (response.__contains__('error') or
                response == None or
                response['data'] == None or
                response['data']['segments'] == None or
                response['data']['segments'][0]['start_time'] == None or
                response['data']['segments'][0]['end_time'] == None
        ):
            # https://stackoverflow.com/questions/1941927/convert-an-rfc-3339-time-to-a-standard-python-timestamp
            # startTime = dt.datetime.strptime(response['data']['segments'][0]['start_time'], '%Y-%m-%dT%H:%M:%SZ')
            # endTime = dt.datetime.strptime(response['data']['segments'][0]['end_time'], '%Y-%m-%dT%H:%M:%SZ')
            startTime = response['data']['segments'][0]['start_time']
            endTime = response['data']['segments'][0]['end_time']
            scheduleDict['name'].append(response['data']['broadcaster_name'])
            scheduleDict['starttime'].append(str(startTime))
            scheduleDict['endtime'].append(str(endTime))
            scheduleDict['duration'].append(
                str (
                    dt.datetime.strptime(response['data']['segments'][0]['end_time'], '%Y-%m-%dT%H:%M:%SZ') -
                    dt.datetime.strptime(response['data']['segments'][0]['end_time'], '%Y-%m-%dT%H:%M:%SZ')
                )
            )
            print(scheduleDict)
            # https://stackoverflow.com/questions/1941927/convert-an-rfc-3339-time-to-a-standard-python-timestamp
            count += 1
        if count == k:
            break
    return scheduleDict
    # print(scheduleDict)


# # get viewers for a specific room
# def getViewerTrendForOneRoom(id):
#     streams = client.get_streams(user_ids = [str(id)])
#     return streams[0]['viewer_count']


