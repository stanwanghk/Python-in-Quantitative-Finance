fileroot = 'C:/Users/WPISH/OneDrive - HKUST Connect 1/Project for DAA/data';
date_index = readtable(fullfile(fileroot,'return_factors/monthly_data/index.csv'));
index = table2array(date_index);
start = 12;
numOfPeriod = length(index);
numOfStock = 207;
alpha_0 = zeros(numOfPeriod-start,numOfStock);
sp_ret = csvread(strcat(fileroot,'/backtest/sp_return.csv'));

for i = start:numOfPeriod
    path = strcat(fileroot,'/estimated_mean_cov/',index(i),{'_return.csv','_cov.csv'});
    path_ret = path{1};
    path_cov = path{2};
    estimated_ret = csvread(path_ret,1);
    estimated_cov = csvread(path_cov,1);
    if i==start
        alpha = initialpos(estimated_cov,estimated_ret',0.0001);
    else
        alpha = portfolio(estimated_cov,estimated_ret',alpha_0(i-start,:),sp_ret(i-start+1));
    end
    alpha_0(i-start+1,:) = alpha';  
    % disp(estimated_ret);
end

path = strcat(fileroot,'/backtest/alpha_sp.csv');
csvwrite(path,alpha_0);