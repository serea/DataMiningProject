# -*- coding: utf-8 -*-
"""
Created on Sat Nov 12 09:57:00 2016

@author: Serea
"""
import pandas
#import pylab
import csv
#from matplotlib import pyplot as plt

file = pandas.read_excel('./hw2data.xls')
#print(file.describe())

dropeddata = file.dropna(axis='rows')
#print(dropeddata.describe())
'''
for head in file:
    file[head].hist()
    pylab.figure(head)
    pylab.show()
'''
del dropeddata['病程阶段']
del dropeddata['转移部位']
del dropeddata['确诊后几年发现转移']

'''
for index,row in dropeddata.iterrows():
    dropeddata['肝气郁结证型系数'][index]=int(row['肝气郁结证型系数']*10)
    dropeddata['热毒蕴结证型系数'][index]=int(row['热毒蕴结证型系数']*10)
    dropeddata['冲任失调证型系数'][index]=int(row['冲任失调证型系数']*10)
    dropeddata['气血两虚证型系数'][index]=int(row['气血两虚证型系数']*10)
    dropeddata['脾胃虚弱证型系数'][index]=int(row['脾胃虚弱证型系数']*10)
    dropeddata['肝肾阴虚证型系数'][index]=int(row['肝肾阴虚证型系数']*10)


print(dropeddata)
'''
with open('continuousdata.csv','w',newline='') as f:
    f_csv = csv.writer(f)
    f_csv.writerow(dropeddata.columns)
    for index,row in dropeddata.iterrows():
        f_csv.writerow(row)
       

