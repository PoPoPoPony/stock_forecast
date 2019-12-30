from selenium import webdriver
from selenium.webdriver.support.ui import Select
import pandas as pd
import bs4
from time import sleep
import os
import numpy as np
import output


path = os.getcwd() + "/data"

def driver_settings(stock_code) : 
	options = webdriver.ChromeOptions()
	options.add_argument("user-agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'")
	prefs = {"profile.managed_default_content_settings.images": 2}
	options.add_experimental_option('prefs' , prefs)
	# , "download.default_directory" : "{}".format(output.check_dir(stock_code))
	return options

def get_stock_info(options , stock_code) : 
	base_url = "https://www.cnyes.com/twstock/ps_historyprice/"
	url = base_url + str(stock_code) + ".htm"
	
	driver = webdriver.Chrome(chrome_options = options)

	res = driver.get(url)
	driver.maximize_window()
	start_date = driver.find_element_by_xpath("//*[@id='ctl00_ContentPlaceHolder1_startText']")
	print(start_date.get_attribute("value"))
	driver.execute_script("arguments[0].value = '2009/01/01';", start_date)

	search_btn = driver.find_element_by_xpath("//*[@id='ctl00_ContentPlaceHolder1_submitBut']")
	search_btn.click()
	driver.minimize_window()

	col_name = []
	data = []

	for i in range(1 , 11) : 
		name = driver.find_element_by_xpath("//*[@id='main3']/div[5]/div[3]/table/tbody/tr[1]/th[" + str(i) + "]")
		col_name.append(name.text)
	else : 
		data.append(col_name)
	
	ct = 1
	table_element = driver.find_element_by_xpath("//*[@id='main3']/div[5]/div[3]/table/tbody")
	 
	temp = []
	try : 
		for i in table_element.text.split("\n") : 
			for j in i.split(" ") :         
				if ct > 10 : 
					ct = 1
					data.append(temp)
					temp = []

				temp.append(j)
				ct += 1
		else : 
			df = pd.DataFrame(data[2 : ] , columns = col_name)
			output.write_csv(df , stock_code , "2207_info")
			driver.close()
			return df
			
	except Exception as e: 
		print(e)
		print("Fail to get stock info，stock_code : {}".format(stock_code))


#因為值一值爆開，所以選擇設其史的第一天為50然後直接正向計算，code在preprocessing.py
def get_KD_value(stock_code , df) : 
	base_url = "https://www.cnyes.com/twstock/Technical/"
	url = base_url + str(stock_code) + ".htm"

	options = webdriver.ChromeOptions()

	options.add_argument("user-agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'")
	prefs = {"profile.managed_default_content_settings.images": 2}
	
	options.add_experimental_option('prefs' , prefs)
	
	driver = webdriver.Chrome(chrome_options = options)

	res = driver.get(url)

	K_lst = []
	D_lst = []
	RSV_lst = []

	recent_K_value = float(driver.find_element_by_xpath("//*[@id='main3']/div[5]/div[3]/table[3]/tbody/tr[2]/td[3]").text)
	recent_D_value = float(driver.find_element_by_xpath("//*[@id='main3']/div[5]/div[3]/table[3]/tbody/tr[2]/td[4]").text)
	recent_day = driver.find_element_by_xpath("//*[@id='main3']/div[5]/cite").text

	driver.quit()
	recent_day = recent_day.replace("-" , "/")
	recent_day_idx = df[df['日期'] == recent_day].index.to_list()[0]

	print(recent_day_idx)

	#暫時假設只會少一天
	if recent_day_idx != 0 : 
		for i in range(recent_day_idx) : 
			RSV_lst.append(((df.iloc[0 , 4] - min(df.iloc[0 : 9 , 3])) / (max(df.iloc[0 : 9 , 2]) - min(df.iloc[0 : 9 , 3]))) * 100)
			K_lst.append(recent_K_value * 2 / 3 + RSV_lst[0] / 3)
			D_lst.append(recent_D_value * 2 / 3 + K_lst[0] / 3)
			
	K_lst.append(recent_K_value)
	D_lst.append(recent_D_value)
	RSV_lst.append(((df.iloc[recent_day_idx , 4] - min(df.iloc[recent_day_idx : recent_day_idx + 9 , 3])) / (max(df.iloc[recent_day_idx : recent_day_idx + 9 , 2]) - min(df.iloc[recent_day_idx : recent_day_idx + 9 , 3]))) * 100)


	#還可以多算一天的KD(-8)
	for i in range(recent_day_idx + 1 , df.shape[0] - 9) : 
		
		K_lst.append((K_lst[i - 1] - RSV_lst[i - 1] / 3) * 1.5)
		D_lst.append((D_lst[i - 1] - K_lst[i - 1] / 3) * 1.5)
		
		near_9days_min = min(df.iloc[i : i + 9 , 3])
		near_9days_max = max(df.iloc[i : i + 9 , 2])

		RSV_lst.append(((df.iloc[i , 4] - near_9days_min) / (near_9days_max - near_9days_min)) * 100)


	df = df.drop(range(df.shape[0] - 9 , df.shape[0]))

	df['K'] = K_lst
	df['D'] = D_lst
	df['RSV'] = RSV_lst


	print(df.columns.to_list())
	print(df.iloc[0 : 30 , :])       
	

def get_PB_value(options , stock_code) : 
	
	driver = webdriver.Chrome(options = options)



	'''
	driver.get("https://www.twse.com.tw/zh/page/trading/exchange/BWIBBU.html")
	
	for i in range(11) : 
		element = driver.find_element_by_xpath("//*[@id='d1']/select[1]")
		year_selector = Select(element)
		year_selector.select_by_index(i)
		for j in reversed(range(11)) : 
			element = driver.find_element_by_xpath("//*[@id='d1']/select[2]")
			month_selector = Select(element)
			month_selector.select_by_index(j)

			stock_code_input = driver.find_element_by_xpath("//*[@id='main-form']/div/div/form/input")
			stock_code_input.send_keys(str(stock_code))

			search_btn = driver.find_element_by_xpath("//*[@id='main-form']/div/div/form/a")
			search_btn.click()

			#ck = driver.find_element_by_xpath('//*[@id="reports"]/div[1]/a[2]')
			#ck.click()

			downloader = driver.find_element_by_xpath("//*[@id='reports']/div[1]/a[2]")
			download_url = downloader.get_attribute("href")
			driver.get(download_url)

			driver.get("https://www.twse.com.tw/zh/page/trading/exchange/BWIBBU.html")
			sleep(1)
	'''
	base_url = "https://www.twse.com.tw/exchangeReport/BWIBBU?response=html&date="
	year_lst = range(2009 , 2020)
	month_lst = ["01" , "02" , "03" , "04" , "05" , "06" , "07" , "08" , "09" , "10" , "11" , "12"]
	url_lst = []

	for i in year_lst : 
		for j in month_lst : 
			url_lst.append(base_url + str(i) + j + "01&stockNo=" + str(stock_code))
	a = []
	for i in url_lst : 
		#driver.get(i)
		df = pd.read_html(i)
		sleep(1)
		a.append(i)

	for i in a : 
		print(i)


get_PB_value(driver_settings(2207) , 2207)


