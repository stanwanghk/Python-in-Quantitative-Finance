from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor as RFreg
import pandas as pd
import settings


def model_select(input_col=['p_var', 'mean_return', 'sum_abs_sent']):
    # data = resample_data.process_all_codes()
    data = pd.read_csv(settings.get_home_path() + 'data/week_data/total.csv', index_col='date')
    indexs = data.index.drop_duplicates()
    # output_col = ['p_var_out']
    file = open(settings.get_home_path() + "data/model_selection.csv", 'w')
    file.write("svr_R^2,rfr_R^2,svr_trend,rfr_trend\n")
    # validation
    svr = SVR(kernel='rbf', C=1e3, gamma=0.1)
    rfr = RFreg()
    val_num = int(len(indexs) / 2)
    # first train data
    train_input = data[data.index == indexs[0]].set_index('code')[input_col]
    train_output = data[data.index == indexs[1]].set_index('code')['p_var']
    train = train_input.join(train_output, rsuffix='_out') 
    train = train.dropna()
    for i in range(1, val_num):
        test_input = data[data.index == indexs[i]].set_index('code')[input_col]
        test_output = data[data.index == indexs[i + 1]].set_index('code')['p_var']
        test = test_input.join(test_output, rsuffix='_out')
        test = test.dropna()
        svr.fit(train[input_col], train.p_var_out.values)
        rfr.fit(train[input_col], train.p_var_out.values)
        test['p_var_pre'] = svr.predict(test[input_col])
        test['p_var_pre2'] = rfr.predict(test[input_col])
        # get the R squared
        print(svr.score(train[input_col], train.p_var_out.values).round(4),
                rfr.score(train[input_col], train.p_var_out.values).round(4))
        # calculate the right rate for predicting trend
        test = test.assign(trend=0)
        test.ix[(test.p_var_out>=test.p_var)&(test.p_var_pre>=test.p_var),'trend'] = 1
        test.ix[(test.p_var_out<=test.p_var)&(test.p_var_pre<=test.p_var),'trend'] = 1
        test = test.assign(trend2=0)
        test.ix[(test.p_var_out>=test.p_var)&(test.p_var_pre2>=test.p_var),'trend2'] = 1
        test.ix[(test.p_var_out<=test.p_var)&(test.p_var_pre2<=test.p_var),'trend2'] = 1
        print(test.trend.mean().round(4),test.trend2.mean().round(4))
        file.write("{},{},{},{}\n".format(svr.score(train[input_col], train.p_var_out.values).round(4),
            rfr.score(train[input_col],train.p_var_out.values).round(4),
            test.trend.mean().round(4),
            test.trend2.mean().round(4)))
        train = test[input_col + ['p_var_out']]
    file.close()
