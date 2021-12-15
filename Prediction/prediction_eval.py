import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.arima.model import ARIMA
from math import sqrt
from trend_prediction import fetch_data


def fig_plot(method_name, time_axis, true_values, pred_values, start_idx):
    plt.figure(figsize=(10, 5))
    plt.plot(time_axis, true_values)
    plt.plot(time_axis, pred_values, ls='--')
    plt.legend(['True values', 'Prediction'])
    plt.xlabel('time')
    plt.ylabel('viewer_count')
    rmse_arima = sqrt(
        mean_squared_error(true_values[start_idx: len(true_values)], pred_values[start_idx: len(pred_values)]))
    print('Root mean squared error (RMSE) of ARIMA method is {}'.format(rmse_arima))
    plt.title('{}            (RMSE = {})'.format(method_name, rmse_arima))
    plt.grid()
    plt.show()


def split_data(_df, start_idx):
    train = _df[0: start_idx]
    test = _df[start_idx: _df.shape[0]]
    return train, test


df = fetch_data('Total')
portion = round(df.shape[0] * 0.8)
train_set, test_set = split_data(df, portion)


# Prophet
m = Prophet(daily_seasonality=True, weekly_seasonality=True, changepoint_prior_scale=0.01).fit(train_set)
future = m.make_future_dataframe(periods=test_set.shape[0], freq='3min')
forecast = m.predict(future)
fig = m.plot(forecast, figsize=(10, 5))
fig.show()
pred_prophet = forecast[['ds', 'yhat']]
rmse_prophet = sqrt(mean_squared_error(test_set['y'].to_numpy(), pred_prophet['yhat'][portion: df.shape[0]]))
fig_plot('Prophet', df['ds'].to_numpy(), df['y'].to_numpy(), pred_prophet['yhat'].to_numpy(), portion)


# ARIMA
model = ARIMA(train_set['y'].to_numpy(), order=(1, 0, 0))
model_fit = model.fit()
pred_arima = model_fit.predict(start=0, end=df.shape[0]-1)
pred_arima = pd.DataFrame(pred_arima, index=df['ds'], columns=['viewer_count'])

fig_plot('ARIMA', df['ds'].to_numpy(), df['y'].to_numpy(), pred_arima['viewer_count'].to_numpy(), portion)
