'''Extract 12-72h level probabilistic prediction'''
import numpy as np
np.random.seed(1337)
import keras
from keras.models import load_model
import h5py
import sklearn
from sklearn.model_selection import train_test_split
from keras.utils import np_utils
import pandas as pd
import os
import csv
import os.path
import math
from time import *
#from function_time_demo import *
from pandas import read_csv
from sklearn.preprocessing import MinMaxScaler
import time as tttt
import datetime
#from interpolate_9_5_ccx_function import *
import sys
#from micaps_function import *
import datetime as dt
def local2utc(local_st):
	'''convert local time to UTC'''
	time_struct = tttt.mktime(local_st.timetuple())
	utc_st = dt.datetime.utcfromtimestamp(time_struct)
	return utc_st
def utc2local(utc_st):
	'''convert UTC to local time'''
	now_stamp = tttt.time()
	local_time = dt.datetime.fromtimestamp(now_stamp)
	utc_time = dt.datetime.utcfromtimestamp(now_stamp)
	offset = local_time - utc_time
	local_st = utc_st + offset
	return local_st

# create a log file
name = os.path.dirname(__file__)
a = os.path.abspath(name)
absu = a+'/'
fsock = open(absu+'12_72_l_p_error.log', 'a')
sys.stderr = fsock
sa = tttt.strftime("%Y%m%d%H%M", tttt.localtime())
ef = open(absu+'12_72_l_p_error.log', 'a')
ef.write('*****************'+str(sa)+'*****************'+'\n')
ef.close()
start = tttt.clock()
sa = tttt.strftime("%Y%m%d%H", tttt.localtime())
#print('begin:',tttt.strftime("%Y%m%d%H", tttt.localtime()))
localtime = tttt.asctime(tttt.localtime(tttt.time()))
time_now = tttt.strftime("%Y%m%d%H%M", tttt.localtime())

# get time
inital_time = tttt.strftime("%Y%m%d%H%M", tttt.localtime())
today = datetime.date.today()
yesterday = today - datetime.timedelta(days = 1)
#if int(inital_time[-4:]) < 820:
#	qibao = str(yesterday)[:4]+str(yesterday)[5:7]+str(yesterday)[8:10]+'00'
#elif int(inital_time[-4:]) < 2120:
#	qibao = str(yesterday)[:4]+str(yesterday)[5:7]+str(yesterday)[8:10]+'12'
#else:
#	qibao = str(today)[:4]+str(today)[5:7]+str(today)[8:10]+'00'
if int(inital_time[-4:]) < 520:
	qibao = str(yesterday)[:4]+str(yesterday)[5:7]+str(yesterday)[8:10]+'00'
elif int(inital_time[-4:]) < 1720:
	qibao = str(yesterday)[:4]+str(yesterday)[5:7]+str(yesterday)[8:10]+'12'
else:
	qibao = str(today)[:4]+str(today)[5:7]+str(today)[8:10]+'00'
#print('#',qibao)
#qibao = '2018030512'
aaa = str(qibao)
bbb = dt.datetime(int(aaa[:4]),int(aaa[4:6]), int(aaa[6:8]), int(aaa[8:10]))
timeaaa = utc2local(bbb)
qibao_local = str(timeaaa)[:4]+str(timeaaa)[5:7]+str(timeaaa)[8:10]+str(timeaaa)[11:13]
#qibao = '2017080412'#test
te = str(inital_time)[:4]+'-'+str(inital_time)[4:6]+'-'+str(inital_time)[6:8]+\
'-'+str(inital_time)[8:10]
inital_time_list = pd.date_range(te,periods = 72,freq = '1h').tolist()
time_list = []
for i in range(len(inital_time_list)):
	time_list.append(str(inital_time_list[i])[:4]+str(inital_time_list[i])[5:7]+\
	str(inital_time_list[i])[8:10]+str(inital_time_list[i])[11:13])

# read path from file
dir_f = open(absu+'12_72_l_p.txt','r')
dir_ff = dir_f.readlines()
pool_name = dir_ff[0].strip('\n')
over_name = dir_ff[1].strip('\n')
os.system('mkdir '+eval(over_name)+inital_time[:-2])

# extract
try:
	for i in range(len(time_list)):
		for j in range(1,7):
			os.system('cp '+eval(pool_name)+qibao_local+'/'+time_list[i]+'finish22.txt'+str(j)\
			+' '+eval(over_name)+inital_time[:-2]+'/')
except:
	#print(time_list[i])
	pass



























