from selenium import webdriver
import pandas as pd
import bs4
from time import sleep
import os

path = os.getcwd() + "/data"


def get_text(stock_code) : 
    
    header = {}
    
    base_url = "https://www.cnyes.com/twstock/ps_historyprice/"
    url = base_url + str(stock_code) + ".htm"
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'")
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
    




    ct = 0
    table_element = driver.find_element_by_xpath("//*[@id='main3']/div[5]/div[3]/table/tbody")
     
    temp = []
    ct = 1
    for i in table_element.text.split("\n") : 
        for j in i.split(" ") :         
            if ct > 10 : 
                ct = 1
                data.append(temp)
                print(temp)
                temp = []

            temp.append(j)
            ct += 1
    else : 
        df = pd.DataFrame(data[2 : ] , columns = col_name)
        df.to_csv(path + "/" + str(stock_code) + ".csv" , encoding = 'big5' , index = False)
        print(df)
        driver.close()


    '''
    for i in range(2 , 2710) : 
        temp = []
        for j in range(1 , 10) : 
            element = driver.find_element_by_xpath("//*[@id='main3']/div[5]/div[3]/table/tbody/tr[" + str(i) + "]/td[" + str(j) + "]")
            temp.append(element.text)
        else : 
            data.append(temp)
            print(temp)
            #ct += 1
    else : 
        df = pd.DataFrame(data)
        print(df)
        
        pd.write_csv(path + "/" + str(stock_code) + ".csv")
    '''


get_text(2207)
get_text(2454)


