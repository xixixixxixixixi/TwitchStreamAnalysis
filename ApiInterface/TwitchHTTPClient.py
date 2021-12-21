# %%
# !/usr/bin/env python
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
import pandas_gbq
from google.oauth2 import service_account
from Prediction.trend_prediction import trend_prediction
import random

# Credentials
client_id = '9tq8ugh8o679ce3bgoa29fhdpwfjbi'
oauth_token = 'b55lks0s75s1xqlcgxe42uyz0p4etw'

client = twitch.TwitchHelix(client_id=client_id, oauth_token=oauth_token)

# Connect Big Query
table_id = 'big-data-analytics-326904.project.top_game_viewers'
credentials = service_account.Credentials.from_service_account_file("key.json")
pandas_gbq.context.credentials = credentials
pandas_gbq.context.project = "big-data-analytics-326904"

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
    streams = client.get_streams(game_ids=gameIds, page_size=100)
    count = 0
    gameDict = {}
    for stream in streams:
        if gameDict.__contains__(stream['game_name']):
            gameDict[stream['game_name']] += stream['viewer_count']
        else:
            gameDict[stream['game_name']] = stream['viewer_count']
        # print(gameDict)
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
        # print(tagDict)
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
                str(
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

def getDynamicHistory(game_list):
    """
    Fetch data from Big Query

    :param game_name: string.
    'Chatting', 'GrandTheftAutoV', 'LeagueofLegends', 'ApexLegends', 'Valorant', CallofDuty', 'Fortnite',
    'TeamfightTactics', 'Minecraft', 'Pokemon', or 'Total'
    :return:
    """
    #
    # {
    #     label: ['lol', 'cod', 'CSGO'],
    #     data: [[1,2,3], [1,2,3], [1,2,3]]
    # }
    # TODO： implement add game list to sql
    SQL = "SELECT * FROM `{}`".format(table_id)
    df = pandas_gbq.read_gbq(SQL)
    print(list(df))
    result = {}
    result["gameLabel"] = list(df)[2: len(list(df))]
    viewer_list = []
    for game in list(df)[2: len(list(df))]:
        viewer_list.append(df[game].to_list())
    result["viewerCount"] = viewer_list
    print(df)
    return result


# getDynamicHistory(['Chatting', 'GrandTheftAutoV', 'LeagueofLegends',
#             'ApexLegends', 'Valorant', 'CallofDuty', 'Fortnite',
#             'TeamfightTactics', 'Minecraft', 'Pokemon'])


def getPrediction(game_name):
    """
    Get trend prediction results.
    :param game_name: string
    :return: dict

     {
         "label": ['True', 'Prediction'],
         "time": ['2021-12-17 00:00:00', '2021-12-17 00:03:00', ...],
         "true": [12322,24322, ...]
         "pred": [12432,25342, ...]
     }

    """
    time, y, yhat, _, _ = trend_prediction(game_name)
    prediction = {'label': ['True', 'Predict'], 'time': time, 'true': y, 'pred': [int(pred) for pred in yhat]}
    return prediction


def getDailyMeanViewerCount():
    game_list = ['Chatting', 'GrandTheftAutoV', 'LeagueofLegends',
                 'ApexLegends', 'Valorant', 'CallofDuty', 'Fortnite',
                 'TeamfightTactics', 'Minecraft', 'Pokemon']

    sql = ', '.join(['avg({}) {}'.format(game, game) for game in game_list])
    sql = "SELECT Date(Time) hour, " + sql + " FROM `{}` ".format(table_id) + "group by hour"

    df = pandas_gbq.read_gbq(sql)
    results = []
    results.append(['time'] + df['hour'].tolist())
    for game in game_list:
        results.append([game] + [str(round(x)) for x in df[game].tolist()])
    # results = {'time': ['time'] + df['hour'].tolist()}
    # for game in game_list:
    #     results[game] = [game] + [str(round(x)) for x in df[game].tolist()]

    return results


def getClipsByUserRequest(user_name):
    user_id = client.get_users(user_name)[0]["id"]
    clips = client.get_clips(user_id)
    clip_list = []
    count = 0
    for clip in clips:
        clip_list.append(clip)
        count += 1
        if count == 10:
            break
    return clip_list


def getWordCloudDataForTopGamesViewerCount(k):
    result_list = []
    topGames = getTopKGames(int(k))
    print(topGames)
    for i in range(0, len(topGames)):
        if i == 0:
            continue
        result_list.append(
            {
                "name": topGames[i][0],
                "value": topGames[i][1]
            }
        )
    return result_list


def getSankeyForGamesViewer(k, m):
    top_games = client.get_top_games()
    count = 0
    node_dict = {}
    for game in top_games:
        if count == k:
            break
        node_dict[game["name"]] = []
        popular_streams = client.get_streams(game_ids=[int(game["id"])])
        stream_count = 0
        for stream in popular_streams:
            # print(stream)
            if stream_count == m:
                break
            node_dict[game["name"]].append([stream["user_name"], stream["viewer_count"]])
            stream_count += 1
        count += 1
    print(node_dict)
    result_dict = {
        "data": [],
        "links": []
    }
    r = lambda: random.randint(0, 255)
    color = '#{:02x}{:02x}{:02x}'.format(r(), r(), r())
    result_dict["data"].append(
        {
            "name": "TopGames",
            "itemStyle": {
                "color": color,
                "borderColor": color
            }
        }
    )
    for node in node_dict:
        # https://stackoverflow.com/questions/13998901/generating-a-random-hex-color-in-python
        r = lambda: random.randint(0, 255)
        color = '#{:02x}{:02x}{:02x}'.format(r(), r(), r())
        result_dict["data"].append(
            {
                "name": node,
                "itemStyle": {
                    "color": color,
                    "borderColor": color
                }
            }
        )
        total_viewer_count_for_a_game = 0
        for stream in node_dict[node]:
            r = lambda: random.randint(0, 255)
            color = '#{:02x}{:02x}{:02x}'.format(r(), r(), r())
            result_dict["data"].append(
                {
                    "name": stream[0],
                    "itemStyle": {
                        "color": color,
                        "borderColor": color
                    }
                }
            )
            result_dict["links"].append(
                {
                    "source": node,
                    "target": stream[0],
                    "value": int(stream[1])
                }
            )
            total_viewer_count_for_a_game += int(stream[1])
        result_dict["links"].append(
            {
                "source": 'TopGames',
                "target": node,
                "value": total_viewer_count_for_a_game
            }
        )
    print(result_dict)
    return result_dict
# getSankeyForGamesViewer(10, 10)
