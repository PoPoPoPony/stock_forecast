import get_data
import pandas as pd
import os

path = os.getcwd()

#df_2207 = get_data.get_stock_info(get_data.driver_settings() , 2207)
#df_2454 = get_data.get_stock_info(get_data.driver_settings() , 2454)
#df = pd.read_csv(path + "/data/2207.csv" , encoding = 'big5')

get_data.get_PB_value(get_data.driver_settings(2207) , 2207)

def KD_value(stock_code) : 
	df = pd.read_csv(path + "/data/" + str(stock_code) + "/" + str(stock_code) + ".csv" , encoding = "big5")
	print(df)
	#K?D????????50
	K_lst = [50]
	D_lst = [50]
	
	#???"?9???????????8????KD?
	for i in reversed(range(df.shape[0] - 8)) : 
		RSV = (df.iloc[i , 4] - min(df.iloc[i : i + 9 , 3])) / (max(df.iloc[i : i + 9 , 2]) - min(df.iloc[i : i + 9 , 3]))
		#K_lst[i - (df.shape[0] - 9)] : ??-9????????K(?lst?????K)
		K_lst.append(K_lst[i - (df.shape[0] - 9)] * 0.67 + RSV * 0.33)
		D_lst.append(D_lst[i - (df.shape[0] - 9)] * 0.67 + K_lst[i - (df.shape[0] - 9) + 1] * 0.33)

	df = df[:df.shape[0] - 7]
	df["K_value"] = list(reversed(K_lst))
	df["D_value"] = list(reversed(D_lst))
	print(df)

print()

