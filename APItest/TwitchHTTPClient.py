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

def getTopK(k):
    streams = client.get_streams()  # APICursor containing Stream objects
    streams_top20 = streams._queue  # List of Stream objects
    fields = ['id', 'user_id', 'user_login', 'user_name', 'game_id', 'game_name', 'type', 'title', 'viewer_count',
              'started_at', 'language', 'thumbnail_url', 'tag_ids', 'is_mature']
    data = {'data': []}
    count = 0
    for stream in streams:
        print(stream)
        d = {}
        for field in fields:
            if field == 'started_at':
                d[field] = stream[field].strftime('%Y-%m-%d %H:%M:%S')
            else:
                d[field] = stream[field]
        data['data'].append(d)
        count += 1
        if count == 49:
            break
    return data

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

