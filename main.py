import web_clawer
import output
import preprocessing
import os
import pandas as pd

path = os.getcwd()

#web_clawer.get_stock_info(web_clawer.driver_settings() , 2207)
#df = preprocessing.concat_inlist_df(web_clawer.get_PB_value(web_clawer.driver_settings() , 2207))
#output.write_csv(df , 2207 , "2207_PB_value")


info_df = pd.read_csv(path + "/data/2207/2207_info.csv" , encoding = "big5")
pb_df = pd.read_csv(path + "/data/2207/2207_PB_value.csv" , encoding = "big5")

info_df , pb_df = preprocessing.match_info_and_PB_value_idx(info_df , pb_df)

[pb_df] = preprocessing.drop_redundant_col([pb_df] , [["日期" , "股利年度" , "財報年/季"]])

info_pb_df = preprocessing.concat_info_pb(info_df , pb_df)

