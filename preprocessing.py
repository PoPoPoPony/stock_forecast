import web_crawler
import pandas as pd
import os
import output

path = os.getcwd()

#df_2207 = get_data.get_stock_info(get_data.driver_settings() , 2207)
#df_2454 = get_data.get_stock_info(get_data.driver_settings() , 2454)
#df = pd.read_csv(path + "/data/2207.csv" , encoding = 'big5')

#計算KD值，輸入df，並將KD兩個欄位輸出成csv，會比原本的df少7個row
def KD_value(df) : 
	
	print(df)
	K_lst = [50]
	D_lst = [50]
	
	for i in reversed(range(df.shape[0] - 8)) : 
		RSV = (df.iloc[i , 4] - min(df.iloc[i : i + 9 , 3])) / (max(df.iloc[i : i + 9 , 2]) - min(df.iloc[i : i + 9 , 3]))
		today_K = K_lst[i - (df.shape[0] - 9)] * 0.67 + RSV * 0.33
		K_lst.append(today_K)
		today_D = D_lst[i - (df.shape[0] - 9)] * 0.67 + today_K * 0.33
		D_lst.append(today_D)

	KD_df = pd.DataFrame(dict(zip(["K_value" , "D_value"] , [list(reversed(K_lst)) , list(reversed(D_lst))])))
	output.write_csv(KD_df , 2207 , "2207_KD_value")

def concat_inlist_df(df_lst) : 
	df = pd.concat([df_lst[0] , df_lst[1]] , axis = 0 , ignore_index = True)
	for i in range(2 , len(df_lst)) : 
		df = pd.concat([df , df_lst[i]] , axis = 0 , ignore_index = True)
	
	return df

def concat_info_and_reversed_df(info_df , reversed_df) : 
	reversed_cols = reversed_df.columns.to_list()

	for i in reversed_cols : 
		info_df[i] = list(reversed(reversed_df[i].to_list()))	

	return info_df	

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

#計算3日RSI、5日RSI、7日RSI、10日RSI
def RSI_value(df) : 
	catch_range_lst = [3 , 5 , 7 , 10]
	fluctuation_lst = df["漲跌"].to_list()
	fluctuation_up_lst = []
	fluctuation_down_lst = []

	for i in fluctuation_lst : 
		if i > 0 : 
			fluctuation_up_lst.append(i)
			fluctuation_down_lst.append(0)
		elif i < 0 : 
			fluctuation_up_lst.append(0)
			fluctuation_down_lst.append(abs(i))
		else : 
			fluctuation_up_lst.append(0)
			fluctuation_down_lst.append(0)

	accumulative_up_lst = []
	accumulative_down_lst = []

	for i in range(len(catch_range_lst)) : 
		#每n個一取，最後就會有n - 1個取不到(沒有資料了)
		temp_lst = []
		for j in range(len(fluctuation_up_lst) - (catch_range_lst[i] - 1)) : 
			temp = 0
			for k in range(catch_range_lst[i]) : 
				temp += fluctuation_up_lst[j + k]
				temp /= catch_range_lst[i]
			temp_lst.append(temp)
		accumulative_up_lst.append(temp_lst)

	for i in range(len(catch_range_lst)) : 
		#每n個一取，最後就會有n - 1個取不到(沒有資料了)
		temp_lst = []
		for j in range(len(fluctuation_down_lst) - (catch_range_lst[i] - 1)) : 
			temp = 0
			for k in range(catch_range_lst[i]) : 
				temp += fluctuation_down_lst[j + k]
				temp /= catch_range_lst[i]
			temp_lst.append(temp)
		accumulative_down_lst.append(temp_lst)

	RSI_lst = []

	for i in range(len(accumulative_up_lst)) : 
		temp_lst = []
		for j in range(len(accumulative_up_lst[i])) : 
			RSI = 100 * accumulative_up_lst[i][j] / (accumulative_up_lst[i][j] + accumulative_down_lst[i][j])
			temp_lst.append(RSI)
		RSI_lst.append(temp_lst)

	#對齊所有尺度的RSI值
	for i in range(3) : 
		RSI_lst[i] = RSI_lst[i][ : len(RSI_lst[3])]

	RSI_df = pd.DataFrame(dict(zip(["3日RSI" , "5日RSI" , "7日RSI" , "10日RSI"] , RSI_lst)))
	
	RSI_up_thrend = []
	RSI_down_thrend = []

	for i in range(RSI_df.shape[0]) : 
		ct = 0
		if RSI_df.iloc[i , 0] > RSI_df.iloc[i , 1] : 
			ct = 1
			if  RSI_df.iloc[i , 1] > RSI_df.iloc[i , 2] : 
				ct = 2
				if RSI_df.iloc[i , 2] > RSI_df.iloc[i , 3] : 
					ct = 3

		RSI_up_thrend.append(ct)

	for i in range(RSI_df.shape[0]) : 
		ct = 0
		if RSI_df.iloc[i , 1] > RSI_df.iloc[i , 0] : 
			ct = 1
			if  RSI_df.iloc[i , 2] > RSI_df.iloc[i , 1] : 
				ct = 2
				if RSI_df.iloc[i , 3] > RSI_df.iloc[i , 2] : 
					ct = 3

		RSI_down_thrend.append(ct)
	
	RSI_df["RSI_up_thrend"] = RSI_up_thrend
	RSI_df["RSI_down_thrend"] = RSI_down_thrend
	
	output.write_csv(RSI_df , 2207 , "2207_RSI_value")

def metal_price_procedure(mp_df) : 
	mp_df.drop(["2" , "4" , "6" , "8"] , axis = 1 , inplace = True)
	mp_df.columns = ["日期" , "黃金賣出牌價" , "黃金買進牌價" , "白金賣出牌價" , "白金買進牌價"]

	#後來發現以前的股市好像是只有禮拜天休息==
	#mp_df = mp_df.loc[~(mp_df['日期'].str.contains("星期六")) , :]

	mp_df.reset_index(inplace = True)
	mp_df.drop("index" , axis = 1 , inplace = True)
	mp_df["日期"] = [x.split("(")[0] for x in mp_df["日期"]]
	
	mp_cols = mp_df.columns.to_list()

	for i in mp_cols : 
		mp_df[i] = list(reversed(mp_df[i].to_list()))	

	return mp_df

def NASDAQ_procedure(df) : 
	df.columns = ["日期" , "NASDAQ開盤價" , "NASDAQ收盤價"]
	
	date = df["日期"].to_list()

	for i in range(len(date)) : 
		(Y , M , D) = date[i].split("/")
		if len(M) == 1 : 
			M = "0" + M
		if len(D) == 1 : 
			D = "0" + D
		date[i] = Y + "/" + M + "/" + D

	df["日期"] = date
	
	return df