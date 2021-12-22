import pmdarima as pm
from prophet import Prophet
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error
from statsmodels.tsa.arima.model import ARIMA
from math import sqrt
from trend_prediction import fetch_data
import pandas as pd
from sklearn.ensemble import RandomForestRegressor


def fig_plot(method_name, time_axis, true_values, pred_values, start_idx):
    plt.figure(figsize=(10, 5))
    plt.plot(time_axis, true_values)
    plt.plot(time_axis[0: start_idx], pred_values[0: start_idx], ls='--')
    plt.plot(time_axis[start_idx:], pred_values[start_idx:], ls='--')
    plt.legend(['True values', 'Fitting', 'Prediction'])
    plt.xlabel('time')
    plt.ylabel('viewer_count')
    rmse = sqrt(
        mean_squared_error(true_values[start_idx: len(true_values)], pred_values[start_idx: len(pred_values)]))
    print('Root mean squared error RMSE of {} method is {}'.format(method_name, rmse))
    mape = mean_absolute_percentage_error(true_values[start_idx: len(true_values)], pred_values[start_idx: len(pred_values)])
    print('Mean absolute percentage error of {} method is {}'.format(method_name, mape))
    plt.title('{}            (RMSE = {}, MAPE = {})'.format(method_name, rmse, mape))
    plt.grid()
    plt.show()


def split_data(_df, start_idx):
    train = _df[0: start_idx]
    test = _df[start_idx: _df.shape[0]]
    return train, test


if __name__ == "__main__":
    df = fetch_data('GrandTheftAutoV')
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
    #
    # # # Seasonal ARIMA
    # # smodel = pm.auto_arima(train_set['y'],
    # #                        start_p=1,
    # #                        start_q=1,
    # #                        test='adf',
    # #                        max_p=3,
    # #                        max_q=3,
    # #                        m=5,
    # #                        start_P=0,
    # #                        seasonal=True,
    # #                        d=None,
    # #                        D=1,
    # #                        trace=True,
    # #                        error_action='ignore',
    # #                        suppress_warnings=True,
    # #                        stepwise=True)
    # # fitted = smodel.predict(n_periods=test_set.shape[0])
    # # pred_sarima = train_set['y'].tolist() + fitted.tolist()
    # # fig_plot('ARIMA', df['ds'].to_numpy(), df['y'].to_numpy(), pred_sarima, portion)
    #
    # ARIMA
    model = ARIMA(train_set['y'], order=(1, 0, 0))
    model_fit = model.fit()
    pred_arima = model_fit.predict(start=1, end=train_set.shape[0])
    pred_arima = pred_arima.tolist()
    forecast = model_fit.forecast(test_set.shape[0])
    forecast = forecast.tolist()

    pred_arima = pred_arima + forecast

    fig_plot('ARIMA', df['ds'].to_numpy(), df['y'].to_numpy(), pred_arima, portion)

    # # RF Regression
    # df = pd.read_csv('RawDataRF.csv')
    # data = df.groupby('time').describe()
    # y = df.groupby('time').sum().reset_index()
    # y['time'] = pd.to_datetime(y['time'])
    # col_name = ['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']
    # data.columns = col_name
    # for i in range(1, 4):
    #     for col in col_name:
    #         c = col + '(t-{})'.format(i)
    #         data[c] = data[col].shift(i)
    # portion = round(data.shape[0] * 0.8)
    # #%%
    # x_train = data[3:portion].iloc[:, [i for i in range(8, 32)]]
    # x_test = data[portion:df.shape[0]].iloc[:, [i for i in range(8, 32)]]
    # #%%
    # y_train = y[3:portion]
    # y_test = y[portion:df.shape[0]]
    #
    # # reg = svm.SVR()
    # reg = RandomForestRegressor(random_state=200)
    # reg.fit(x_train, y_train['viewer_count'])
    # y_pred = reg.predict(x_test)
    # y_pred = pd.DataFrame(y_pred, index=y_test['time'], columns=['viewer_count']).reset_index()
    # fig_plot('RF Forest', y_train['time'].tolist() + y_test['time'].tolist(),
    #          y_train['viewer_count'].tolist() + y_test['viewer_count'].tolist(),
    #          y_train['viewer_count'].tolist() + y_pred['viewer_count'].tolist(), portion)
