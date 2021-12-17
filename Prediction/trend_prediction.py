import pandas_gbq
from google.oauth2 import service_account
from prophet import Prophet

credentials = service_account.Credentials.from_service_account_file('key.json')
table_id = 'big-data-analytics-326904.project.top_game_viewers'

pandas_gbq.context.credentials = credentials
pandas_gbq.context.project = "big-data-analytics-326904"


def fetch_data(game_name):
    """
    Fetch data from Big Query

    :param game_name: string.
    'Chatting', 'GrandTheftAutoV', 'LeagueofLegends', 'ApexLegends', 'Valorant', CallofDuty', 'Fortnite',
    'TeamfightTactics', 'Minecraft', 'Pokemon', or 'Total'
    :return: dataframe, column name = ['ds', 'y']
    """

    SQL = "SELECT Time, {} FROM `{}` order by Time".format(game_name, table_id)
    df = pandas_gbq.read_gbq(SQL)
    df = df.rename(columns={'Time': 'ds', game_name: 'y'})

    return df


def trend_prediction(game_name):
    df = fetch_data(game_name)
    m = Prophet(daily_seasonality=True, weekly_seasonality=True, changepoint_prior_scale=0.01).fit(df)
    future = m.make_future_dataframe(periods=200, freq='3min')
    forecast = m.predict(future)
    prediction = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
    print(prediction)
    fig = m.plot(forecast)
    fig.show()

    return (prediction['ds'].tolist(),
            df['y'].tolist(),
            prediction['yhat'].tolist(),
            prediction['yhat_lower'].tolist(),
            prediction['yhat_upper'].tolist())


if __name__ == "__main__":
    time, y, yhat, yhat_lower, yhat_upper = trend_prediction('GrandTheftAutoV')
