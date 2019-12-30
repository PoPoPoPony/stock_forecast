import pandas as pd
import os

path = os.getcwd()

def check_dir(dir_name) : 
	dir_path = path + "/data/" + str(dir_name)
	if not os.path.isdir(dir_path):
		os.mkdir(dir_path)

	return dir_path
	
def write_csv(df , stock_code , file_name) : 
	dir_path = check_dir(stock_code)
	df.to_csv(dir_path + "/" + str(file_name) + ".csv" , encoding = 'big5' , index = False)