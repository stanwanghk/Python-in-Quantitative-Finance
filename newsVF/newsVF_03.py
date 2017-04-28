import volatility_analysis.volatility_forecast as vf

vf.garch()
input_col = ['p_var', 'mean_return']
file_name = 'garch'
vf.garch(input_col, file_name)
