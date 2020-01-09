import web_crawler
import output
import preprocessing
import os
import pandas as pd

path = os.getcwd()

'''
web_crawler.get_stock_info(web_crawler.driver_settings() , 2207)

df = preprocessing.concat_inlist_df(web_crawler.get_PB_value(web_crawler.driver_settings() , 2207))
output.write_csv(df , 2207 , "2207_PB_value")

df = preprocessing.concat_inlist_df(web_crawler.get_tw_market_value(web_crawler.driver_settings()))
output.write_csv(df , "market value" , "tw_market_value")

df = preprocessing.concat_inlist_df(web_crawler.get_tw_market_value(web_crawler.driver_settings()))
output.write_csv(df , "market value" , "tw_market_value")

df = preprocessing.concat_inlist_df(web_crawler.get_gold_price())
output.write_csv(df , "metal price" , "metal_price")
'''

'''
info_df = pd.read_csv(path + "/data/2207/2207_info.csv" , encoding = "big5")
pb_df = pd.read_csv(path + "/data/2207/2207_PB_value.csv" , encoding = "big5")
mv_df = pd.read_csv(path + "/data/market value/tw_market_value.csv" , encoding = "big5")
mp_df = pd.read_csv(path + "/data/metal price/metal_price.csv" , encoding = "big5")
NASDAQ_df = pd.read_csv(path + "/data/NASDAQ/NASDAQ.csv")

mv_df.drop([0] , axis = 0 , inplace = True)
info_df , pb_df = preprocessing.match_info_and_PB_value_idx(info_df , pb_df)

[pb_df , mv_df] = preprocessing.drop_redundant_col([pb_df , mv_df] , [["日期" , "股利年度" , "財報年/季"] , ["日期" , "最高指數" , "最低指數"]])


info_df = preprocessing.concat_info_and_reversed_df(info_df , pb_df)
info_df = preprocessing.concat_info_and_reversed_df(info_df , mv_df)
mp_df = preprocessing.metal_price_procedure(mp_df)

info_df = pd.merge(info_df , mp_df , how = "left")

NASDAQ_df = preprocessing.NASDAQ_procedure(NASDAQ_df)
info_df = pd.merge(info_df , NASDAQ_df , how = "left")

preprocessing.KD_value(info_df)
preprocessing.RSI_value(info_df)
preprocessing.MACD_value(info_df)

KD_df = pd.read_csv(path + "/data/2207/2207_KD_value.csv" , encoding = "big5")
RSI_df = pd.read_csv(path + "/data/2207/2207_RSI_value.csv" , encoding = "big5")
MACD_df = pd.read_csv(path + "/data/2207/2207_MACD_value.csv" , encoding = "big5")

df = preprocessing.concat_technical_index(info_df , [KD_df , RSI_df , MACD_df])
'''

#output.write_csv(df , 2207 , "2207_full_data")

df = pd.read_csv(path + "/data/2207/2207_full_data.csv" , encoding = "big5")
df.drop(["日期" , "漲%"] , axis = 1 , inplace = True)
preprocessing.convert_string_col(df)
Y_df = df[["漲跌"]]
print(Y_df)
#preprocessing.compute_corr(df)
df = preprocessing.drop_low_corr(df , 20)
scaled_df = preprocessing.standardizer(df)
#mean_df = preprocessing.fill_na_by_mean(df)
#reg_df = preprocessing.fill_na_by_regression(df)


