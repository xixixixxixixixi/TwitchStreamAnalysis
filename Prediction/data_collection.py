from datetime import datetime, timedelta
from textwrap import dedent
import pytz

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

# Twitch data collection
from google.cloud import bigquery
from twitchAPI.twitch import Twitch

# Credentials
# TODO: According to what TA said, we should delete any token included in our project.
#  Note that the content of key.json is deleted for security reason, please contact us if you want to reproduce this project
client_id = 'TWITCH APP CLIENT ID'
app_secret = 'TWITCH APP SECRET'


# Twitch API
twitch = Twitch(client_id, app_secret)
# add App authentication
twitch.authenticate_app([])


# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'chaoying',
    'depends_on_past': False,
    'email': ['cz2617@columbia.edu'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=30),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'sla_miss_callback': yet_another_function,
    # 'trigger_rule': 'all_success'
}


top_games = [['509658', 'Chatting'], ['32982', 'GrandTheftAutoV'], ['21779', 'LeagueofLegends'],
             ['511224', 'ApexLegends'], ['516575', 'Valorant'], ['512710', 'CallofDuty'], 
             ['33214', 'Fortnite'], ['513143', 'TeamfightTactics'], ['27471', 'Minecraft'], ['1584745140', 'Pokemon']]

# ['509658', 'Just Chatting'], ['32982', 'Grand Theft Auto V'], ['21779', 'League of Legends'],
# ['511224', 'Apex Legends'], ['516575', 'VALORANT'], ['512710', 'Call of Duty: Warzone'],
# ['33214', 'Fortnite'], ['513143', 'Teamfight Tactics'], ['27471', 'Minecraft'],
# ['1584745140', 'Pokémon Brilliant Diamond/Shining Pearl']

t = datetime.now(tz=pytz.timezone('US/Eastern')).strftime("%Y-%m-%d %H:%M:%S")


def get_stream_info(game_id, ti):
    """

    Get streams information of every game via Twitch API
    Compute the total viewer count and pass it to next task

    """
    cursor = 'start'
    viewer_count = 0
    stop_flag = False
    while not stop_flag:
        try:
            if cursor == 'start':
                dic = twitch.get_streams(game_id=game_id)
            else:
                dic = twitch.get_streams(after=cursor, game_id=game_id)

            for stream in dic['data']:
                # ignore games with less than 5 viewers
                if stream['viewer_count'] < 5:
                    stop_flag = True
                    print('Less than 5 viewers')
                    break
                else:
                    viewer_count += stream['viewer_count']
            cursor = dic['pagination']['cursor']
        except KeyError:
            break

    ti.xcom_push(key=game_id, value=viewer_count)


def combine(**kwargs):
    """
    Combine the viewer count to

    {'time':  YYYY-MM-DD HH:mm:SS, 'game_name1': viewer_count1, ..., 'game_name10': viewer_count10}

    """
    data = {'Time': t}
    total = 0
    for game in top_games:
        count = kwargs['ti'].xcom_pull(key=game[0], task_ids=game[1])
        data[game[1]] = count
        total += count
    data['Total'] = total

    kwargs['ti'].xcom_push(key='all_streams', value=data)


def schema_def(games):
    """
    Generate Big Query schema

    :param games: list of ['game_id', 'game_name']
    :return: Big Query schema
    """

    schema = [bigquery.SchemaField('Time', "DATETIME"), bigquery.SchemaField('Total', "INTEGER")]
    for game in games:
        schema.append(bigquery.SchemaField(game[1], "INTEGER"))
    return schema


def save_to_bq(**kwargs):
    """
    Save data to Big Query

    """

    # Construct a BigQuery client object.
    bq_client = bigquery.Client()

    data = [kwargs['ti'].xcom_pull(key='all_streams', task_ids='Combination')]

    # Load data to bigquery
    # TODO: According to what TA said, we should delete any token included in our project.
    #  Note that the content of key.json is deleted for security reason, please contact us if you want to reproduce this project
    table_id = 'YOUR GCP BIG QUERY TABLE ID'

    schema = schema_def(top_games)

    job_config = bigquery.LoadJobConfig(
        schema=schema,
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
    )

    load_job = bq_client.load_table_from_json(
        data,
        table_id,
        job_config=job_config,
    )  # Make an API request.

    load_job.result()  # Waits for the job to complete.

    destination_table = bq_client.get_table(table_id)
    print("Loaded {} rows.".format(destination_table.num_rows))


with DAG(
        'Project-Demo',
        default_args=default_args,
        description='DAG for Project',
        schedule_interval=timedelta(minutes=3),
        start_date=datetime(2021, 1, 1),
        catchup=False,
        tags=['project'],
) as dag:
    # t* examples of tasks created by instantiating operators

    chatting = PythonOperator(
        task_id='Chatting',
        python_callable=get_stream_info,
        op_kwargs={'game_id': '509658'},
    )

    grandTheftAutoV = PythonOperator(
        task_id='GrandTheftAutoV',
        python_callable=get_stream_info,
        op_kwargs={'game_id': '32982'},
    )

    leagueOfLegends = PythonOperator(
        task_id='LeagueofLegends',
        python_callable=get_stream_info,
        op_kwargs={'game_id': '21779'},
    )

    apexLegends = PythonOperator(
        task_id='ApexLegends',
        python_callable=get_stream_info,
        op_kwargs={'game_id': '511224'},
    )

    valorant = PythonOperator(
        task_id='Valorant',
        python_callable=get_stream_info,
        op_kwargs={'game_id': '516575'},
    )

    callOfDuty = PythonOperator(
        task_id='CallofDuty',
        python_callable=get_stream_info,
        op_kwargs={'game_id': '512710'},
    )

    fortnite = PythonOperator(
        task_id='Fortnite',
        python_callable=get_stream_info,
        op_kwargs={'game_id': '33214'},
    )

    teamFightTactics = PythonOperator(
        task_id='TeamfightTactics',
        python_callable=get_stream_info,
        op_kwargs={'game_id': '513143'},
    )

    minecraft = PythonOperator(
        task_id='Minecraft',
        python_callable=get_stream_info,
        op_kwargs={'game_id': '27471'},
    )

    pokemon = PythonOperator(
        task_id='Pokemon',
        python_callable=get_stream_info,
        op_kwargs={'game_id': '1584745140'},
    )

    combination = PythonOperator(
        task_id='Combination',
        python_callable=combine,
    )

    streamToBigQuery = PythonOperator(
        task_id='SaveStreamsToBigQuery',
        python_callable=save_to_bq,
    )


    # task dependencies

    [chatting, grandTheftAutoV, leagueOfLegends, apexLegends, valorant, callOfDuty, fortnite,
     teamFightTactics, minecraft, pokemon] >> combination
    combination >> streamToBigQuery
