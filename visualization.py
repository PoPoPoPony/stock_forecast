# -*- coding: utf-8 -*-
"""
Created on Sat Jan  4 21:37:11 2020

@author: USER
"""

import pandas as pd
from datetime import datetime
import csv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

df = pd.read_csv('2207_leo.csv',encoding='big5')
print(df)

df['日期'] = df['日期'].map(lambda x:datetime.strptime(str(x),'%Y/%m/%d'))
x1 = df['日期']
y1 = df['最高']
y2 = df['最低']
#調整fig大小
fig1 = plt.figure(figsize=[20,16])
ax1 = fig1.add_axes([0,0,1,1])

plt.plot(x1,y1,color='b')
plt.plot(x1,y2,color='r',linestyle='--')
plt.title("2207_info",fontsize=30)

plt.show()