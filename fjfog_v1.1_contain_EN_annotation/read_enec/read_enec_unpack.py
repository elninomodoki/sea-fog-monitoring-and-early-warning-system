# -*- coding: utf-8 -*-
'''
Created at 20180306, revised at 20190425
@author: lxb
unpack'''
import numpy as np
np.random.seed(1337)
import pandas as pd
import os
import csv
import os.path
import math
from time import *
from function_time_demo import all_path
from pandas import read_csv
import time as tttt
import datetime
import sys
from multiprocessing import Pool

print('read_enec_unpack_begin')

# record error
name = os.path.dirname(__file__)
a = os.path.abspath(name)
absu = a+'/'
fsock = open(absu+'error_unpack.log', 'a')
#sys.stderr = fsock
sa = tttt.strftime("%Y%m%d%H%M", tttt.localtime())
ef = open(absu+'error_unpack.log', 'a')
ef.write('*****************'+str(sa)+'*****************'+'\n')
ef.close()

# get current time
inital_time = tttt.strftime("%Y%m%d%H%M", tttt.localtime())
today = datetime.date.today()
yesterday = today - datetime.timedelta(days = 1)

# handling time gap
if int(inital_time[-4:]) <= 510:
	qibao = str(yesterday)[:4]+str(yesterday)[5:7]+str(yesterday)[8:10]+'12'
else:
	qibao = str(today)[:4]+str(today)[5:7]+str(today)[8:10]+'00'

############test##########
#test
#qibao = '2018031000'
##########################

# format initial time
te = str(qibao)[:4]+'-'+str(qibao)[4:6]+'-'+str(qibao)[6:8]+\
'-'+str(qibao)[8:10]
# generate time series
inital_time_list = pd.date_range(te,periods = 40,freq = '6h').tolist()
time_list = []
for i in range(len(inital_time_list)):
	time_list.append(str(inital_time_list[i])[:4]+str(inital_time_list[i])[5:7]+\
	str(inital_time_list[i])[8:10]+str(inital_time_list[i])[11:13])

time_list_w = []
for i in range(len(time_list)):
	time_list_w.append(qibao[4:]+'00'+time_list[i][4:]+'001')


# read path from file
dir_f = open(absu+'read_enec_unpack.txt','r')
dir_ff = dir_f.readlines()
wrf_name = dir_ff[0].strip('\n')

father_list = all_path(eval(wrf_name)+qibao) 
print(len(father_list))
# unpack
def unpack(i):
	print('upack-'+str(i))
	if father_list[i][-1] == 'o':
		os.remove(eval(wrf_name)+qibao+'/'+father_list[i])
	else:
		os.system('bzip2 -d '+eval(wrf_name)+qibao+'/'+father_list[i])
	return 0

# mutithreading
pool = Pool(processes=8) 
res = pool.map(unpack, range(len(father_list)))

##test
#unpack(0)
#unpack(1)

print('begin:',sa)
print('over:',tttt.strftime("%Y%m%d%H%M", tttt.localtime()))
print('read_enec_unpack_over')






















