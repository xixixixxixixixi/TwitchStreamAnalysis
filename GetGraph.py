from pyspark import SparkConf, SparkContext
# [
#         #                 {'id': '40230484139', 'user_id': '83232866', 'user_login': 'ibai', 'user_name': 'ibai',
#         #                  'game_id': '518203', 'game_name': 'Sports', 'type': 'live', 'title': 'PADEL DE LAS ESTRELLAS 2 | EL TORNEO DE PADEL DEL AÑO ',
#         #                  'viewer_count': 112452, 'started_at': '2021-11-18 18:13:47', 'language': 'es',
#         #                  'thumbnail_url': 'https://static-cdn.jtvnw.net/previews-ttv/live_user_ibai-{width}x{height}.jpg',
#         #                  'tag_ids': ['d4bb9c58-2141-4881-bcdc-3fe0505457d1'], 'is_mature': False}
#         #
# #             ]

def gameAndViewerGraph(roomList):
    # TODO: finish spark calculation
    # conf = SparkConf().setAppName("test").setMaster("local")
    # sc = SparkContext(conf=conf)
    # data = sc.parallelize(roomList)
    # print(data)
    gameList = []
    print(roomList)
    for room in roomList:
        gameList.append({
            'gameName': room['game_name'],
            'peopleNum': room['viewer_count']
        })
    return gameList

def TrendOfOneRoomGraph(roomList):
    # TODO: finish spark calculation
    # conf = SparkConf().setAppName("test").setMaster("local")
    # sc = SparkContext(conf=conf)
    # data = sc.parallelize(roomList)
    # print(data)
    gameList = []
    print(roomList)
    for room in roomList:
        gameList.append({
            'gameName': room['game_name'],
            'peopleNum': room['viewer_count']
        })

# gameAndViewerGraph([])
