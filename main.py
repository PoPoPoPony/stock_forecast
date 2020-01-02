import web_clawer
import output
import preprocessing




df = preprocessing.concat_inlist_df(web_clawer.get_PB_value(web_clawer.driver_settings() , 2207))
output.write_csv(df , 2207 , "2207_PB_value")

print(df)