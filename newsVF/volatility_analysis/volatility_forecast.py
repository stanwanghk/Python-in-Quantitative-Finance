from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor as RFreg
import pandas as pd
import settings


def garch(input_col=['p_var', 'mean_return', 'sum_abs_sent'],
          file_name='modified_grach'):
    # data = resample_data.process_all_codes()
    data = pd.read_csv(settings.get_home_path() +
                       'data/week_data/total.csv', index_col='date')
    indexs = data.index.drop_duplicates()
    # output_col = ['p_var_out']
    file = open(settings.get_home_path() +
                'data/{}.csv'.format(file_name), 'w')
    file.write(
        "time_winodw_forecast_output,time_window_forecast_input,svr_R^2,rfr_R^2,\
        svr_trend,rfr_trend\n")
    # validation
    svr = SVR(kernel='rbf', C=64, gamma=1 / 3)
    rfr = RFreg()

    # the first train data
    train_input = data[data.index == indexs[0]].set_index('code')[input_col]
    train_output = data[data.index == indexs[1]].set_index('code')['p_var']
    train = train_input.join(train_output, rsuffix='_out')
    train = train.dropna()
    for i in range(1, len(indexs)-2):
        test_input = data[data.index == indexs[i]].set_index('code')[input_col]
        test_output = data[data.index == indexs[
            i + 1]].set_index('code')['p_var']
        test = test_input.join(test_output, rsuffix='_out')
        test = test.dropna()
        svr.fit(train[input_col], train.p_var_out.values)
        rfr.fit(train[input_col], train.p_var_out.values)
        test['p_var_pre'] = svr.predict(test[input_col])
        test['p_var_pre2'] = rfr.predict(test[input_col])
        # get the R squared
        r1 = svr.score(train[input_col], train.p_var_out.values).round(4)
        r2 = rfr.score(train[input_col], train.p_var_out.values).round(4)
        # calculate the right rate for predicting trend
        test = test.assign(trend=0)
        test.ix[(test.p_var_out >= test.p_var) & (
            test.p_var_pre >= test.p_var), 'trend'] = 1
        test.ix[(test.p_var_out <= test.p_var) & (
            test.p_var_pre <= test.p_var), 'trend'] = 1
        test = test.assign(trend2=0)
        test.ix[(test.p_var_out >= test.p_var) & (
            test.p_var_pre2 >= test.p_var), 'trend2'] = 1
        test.ix[(test.p_var_out <= test.p_var) & (
            test.p_var_pre2 <= test.p_var), 'trend2'] = 1
        t1 = test.trend.mean().round(4)
        t2 = test.trend2.mean().round(4)
        file.write("{},{},{},{},{},{}\n".format(
            indexs[i + 1], indexs[i], r1, r2, t1, t2))
        # save all predict vol
        out = test[['p_var_pre', 'p_var_pre2', 'p_var_out']]
        out = out.assign(date=indexs[i + 1])
        out.to_csv(settings.get_home_path() +
                   'data/total_predict_{}.csv'.format(file_name),
                   mode='a', header=False, float_format='%.3f')
        train = test[input_col + ['p_var_out']]
        print("finish: ", indexs[i])
    file.close()
