import web_crawler
import pandas as pd
import os
import output
from sklearn.preprocessing.imputation import Imputer
import numpy as np
from sklearn import tree
from sklearn.preprocessing import StandardScaler



path = os.getcwd()

#df_2207 = get_data.get_stock_info(get_data.driver_settings() , 2207)
#df_2454 = get_data.get_stock_info(get_data.driver_settings() , 2454)
#df = pd.read_csv(path + "/data/2207.csv" , encoding = 'big5')

#計算KD值，輸入df，並將KD兩個欄位輸出成csv，會比原本的df少7個row，順序是2019 -> 2009
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

def concat_technical_index(df , technical_df_lst) : 
	min_len = df.shape[0]
	for i in technical_df_lst : 
		if i.shape[0] < min_len : 
			min_len = i.shape[0]

	df = df[ : min_len]
	df_cols = df.columns.to_list()

	for i in range(len(technical_df_lst)) : 
		technical_df_lst[i] = technical_df_lst[i][ : min_len]
		for j in technical_df_lst[i].columns : 
			df_cols.append(j)

	for i in technical_df_lst : 
		df = pd.concat([df , i] , axis = 1 , ignore_index = True)

	df.columns = df_cols

	return df

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

#計算3日RSI、5日RSI、7日RSI、10日RSI，順序應該是2019 -> 2009
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

def MACD_value(df) : 
	#構建出的list都是由2009年進展到2019年
	DI_lst = []
	EMA12_lst = []
	EMA26_lst = []

	for i in reversed(range(df.shape[0])) : 
		DI_lst.append((df.iloc[i , 2] + df.iloc[i , 3] + 2 * df.iloc[i , 4]) / 4)
	
	for i in range(11 , len(DI_lst)) :
		EMA12_lst.append(sum(DI_lst[i - 11 : i + 1]) / 12)
		
	for i in range(25 , len(DI_lst)) : 
		EMA26_lst.append(sum(DI_lst[i - 25 : i + 1]) / 26)

	#EMA平滑化
	for i in range(1 , len(EMA12_lst)) : 
		EMA12_lst[i] = EMA12_lst[i - 1] * 11 / 13 + DI_lst[11 : ][i] * 2 / 13

	for i in range(1 , len(EMA26_lst)) : 
		EMA26_lst[i] = EMA26_lst[i - 1] * 25 / 27 + DI_lst[25 : ][i] * 2 / 27

	#丟棄第一天
	EMA12_lst.pop(0)
	EMA26_lst.pop(0)	

	EMA12_lst = EMA12_lst[len(EMA12_lst) - len(EMA26_lst) : ]

	DIF_lst = []
	for i in range(len(EMA12_lst)) : 
		DIF_lst.append(EMA12_lst[i] - EMA26_lst[i])

	first_MACD = sum(DIF_lst[:9]) / 9
	MACD_lst = [first_MACD]

	for i in range(len(DIF_lst[10:])) : 
		MACD_lst.append(MACD_lst[i - 1] * 4 / 5 + DIF_lst[i] / 5)

	#丟棄前9天，使其與MACD_lst的長度保持一致
	DIF_lst = DIF_lst[9:]

	df = pd.DataFrame(dict(zip(["DIF" , "MACD"] , [list(reversed(DIF_lst)) , list(reversed(MACD_lst))])))

	MACD_buy = []
	MACD_sell = []

	for i in range(1 , df.shape[0]) : 
		if df.iloc[i - 1 , 0] < df.iloc[i - 1 , 1] : 
			if df.iloc[i , 0] > df.iloc[i , 1] : 
				MACD_buy.append(1)
			else : 
				MACD_buy.append(0)
		else : 
			MACD_buy.append(0)
		
		if df.iloc[i - 1 , 0] > df.iloc[i - 1 , 1] : 
			if df.iloc[i , 0] < df.iloc[i , 1] : 
				MACD_sell.append(1)
			else : 
				MACD_sell.append(0)
		else : 
			MACD_sell.append(0)

	df.drop(0 , axis = 0 , inplace = True)
	df["MACD_buy"] = MACD_buy
	df["MACD_sell"] = MACD_sell

	output.write_csv(df , 2207 , "2207_MACD_value")

#因為有兩個column是string，且他中間有"，"，無法直接convert，故寫成一個function
def convert_string_col(df) : 
	temp = []
	temp2 = []
	for i in range(len(df["成交量"].to_list())) : 
		s = df.iloc[i , 5].replace("," , "")
		temp.append(float(s))
		s = df.iloc[i , 6].replace("," , "")
		temp2.append(float(s))
	
	df["成交量"] = temp
	df["成交金額"] = temp2

	return df

#股市的變數相關係數都滿小的，所以目前先全部變數都取
def compute_corr(df) : 
	cor_df = df.corr()
	corr_info = cor_df['收盤'].abs().sort_values(ascending = False).index.to_list()[1 : ]
	print(corr_info)

	return cor_df
	
#保留remain_count數量的column(取corr前n高的)
def drop_low_corr(df , remain_count) : 
	cor_df = df.corr()
	remain_col = cor_df['收盤'].abs().sort_values(ascending = False).index.to_list()[ : remain_count + 1][1 : ]
	df = df[remain_col]

	return df

#會遇到連續兩個空值，若上一個也為空值，則取上上個，以此類推
def fill_na_by_mean(df) : 
	loss_matrix = np.where(np.isnan(df))
	for i in range(len(loss_matrix[0])) : 
		if np.isnan(df.iloc[loss_matrix[0][i] - 1 , loss_matrix[1][i]]) : 
			df.iloc[loss_matrix[0][i] , loss_matrix[1][i]] = (df.iloc[loss_matrix[0][i] - 2 , loss_matrix[1][i]] + df.iloc[loss_matrix[0][i] + 1 , loss_matrix[1][i]]) / 2
		elif np.isnan(df.iloc[loss_matrix[0][i] + 1 , loss_matrix[1][i]]) : 
			df.iloc[loss_matrix[0][i] , loss_matrix[1][i]] = (df.iloc[loss_matrix[0][i] - 1 , loss_matrix[1][i]] + df.iloc[loss_matrix[0][i] + 2 , loss_matrix[1][i]]) / 2
		else : 
			df.iloc[loss_matrix[0][i] , loss_matrix[1][i]] = (df.iloc[loss_matrix[0][i] - 1 , loss_matrix[1][i]] + df.iloc[loss_matrix[0][i] + 1 , loss_matrix[1][i]]) / 2

	return df

def fill_na_by_regression(df) : 
	col_lst = ["黃金賣出牌價" , "黃金買進牌價" , "白金賣出牌價" , "白金買進牌價" , "NASDAQ開盤價" , "NASDAQ收盤價"]

	for i in col_lst : 
		data_order = list(range(df[i].shape[0]))
		loss_idx = np.where(np.isnan(df[i]))[0] 
		data_order = [x for x in data_order if x not in loss_idx]
		
		imp = tree.DecisionTreeRegressor()
		imp.fit(np.array(data_order).reshape(-1 , 1) , df.loc[data_order , i])
		result = imp.predict(np.array(loss_idx).reshape(-1 , 1))

		for j in range(len(result)) : 
			df.loc[loss_idx[j] , i] = result[j]

	return df

def standardizer(df) : 
	status_col = []

	for i in df.columns : 
		if df[i].nunique() < 10 : 
			status_col.append(i)
	
	print(status_col)

	status_df = df[status_col]
	df.drop(status_col , axis = 1 , inplace = True)

	mm = StandardScaler()
	scaled_df = pd.DataFrame(mm.fit_transform(df) , columns = df.columns)
	scaled_df = pd.concat([scaled_df , status_df] , axis = 1)

	return scaled_df




		
		
