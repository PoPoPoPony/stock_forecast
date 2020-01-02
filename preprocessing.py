import web_clawer
import pandas as pd
import os

path = os.getcwd()

#df_2207 = get_data.get_stock_info(get_data.driver_settings() , 2207)
#df_2454 = get_data.get_stock_info(get_data.driver_settings() , 2454)
#df = pd.read_csv(path + "/data/2207.csv" , encoding = 'big5')


def KD_value(stock_code) : 
	df = pd.read_csv(path + "/data/" + str(stock_code) + "/" + str(stock_code) + "_info.csv" , encoding = "big5")
	print(df)

	K_lst = [50]
	D_lst = [50]
	

	for i in reversed(range(df.shape[0] - 8)) : 
		RSV = (df.iloc[i , 4] - min(df.iloc[i : i + 9 , 3])) / (max(df.iloc[i : i + 9 , 2]) - min(df.iloc[i : i + 9 , 3]))

		K_lst.append(K_lst[i - (df.shape[0] - 9)] * 0.67 + RSV * 0.33)
		D_lst.append(D_lst[i - (df.shape[0] - 9)] * 0.67 + K_lst[i - (df.shape[0] - 9) + 1] * 0.33)

	df = df[:df.shape[0] - 7]
	df["K_value"] = list(reversed(K_lst))
	df["D_value"] = list(reversed(D_lst))
	print(df)

def concat_inlist_df(df_lst) : 
	df = pd.concat([df_lst[0] , df_lst[1]] , axis = 0 , ignore_index = True)
	for i in range(2 , len(df_lst)) : 
		df = pd.concat([df , df_lst[i]] , axis = 0 , ignore_index = True)
	
	return df

def concat_info_pb(info_df , pb_df) : 
	pb_cols = pb_df.columns.to_list()

	for i in pb_cols : 
		info_df[i] = list(reversed(pb_df[i].to_list()))	

	return info_df	

def RSI_value(stock_code) : 
	df = pd.read_csv(path + "/data/" + str(stock_code) + "/" + str(stock_code) + ".csv" , encoding = "big5")
	
def match_info_and_PB_value_idx(info_df , pb_df) : 
	if info_df.shape[0] == pb_df.shape[0] : 
		print("info_df and pb_df have same rows")
		return info_df , pb_df

	else : 
		pb_df.drop(0 , axis = 0 , inplace = True)
		return info_df , pb_df

def drop_redundant_col(*kwargs) : 
	for i in range(len(kwargs[0])) : 
		kwargs[0][i].drop(kwargs[1][i] , axis = 1 , inplace = True)

	return kwargs[0]