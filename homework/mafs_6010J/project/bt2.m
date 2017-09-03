actual_ret = csvread(strcat(fileroot,'/backtest/actual_return.csv'),1);
t=alpha_0(1:228,:);
perform = t*actual_ret';
perform = diag(perform);
csvwrite(strcat(fileroot,'/backtest/perfom_sp.csv'),perform);