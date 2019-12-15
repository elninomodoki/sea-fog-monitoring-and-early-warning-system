
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
from function_time_demo import *
from pandas import read_csv
from sklearn.preprocessing import MinMaxScaler
import time as tttt
import datetime
from interpolate_9_5_ccx_function import *
import sys
from micaps_function import *
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
print('predict_lwc_begin')
name = os.path.dirname(__file__)
a = os.path.abspath(name)
absu = a+'/'
fsock = open(absu+'predict_lwc_error.log', 'a')
sys.stderr = fsock
sa = tttt.strftime("%Y%m%d%H%M", tttt.localtime())
ef = open(absu+'predict_lwc_error.log', 'a')
ef.write('*****************'+str(sa)+'*****************'+'\n')
ef.close()
localtime = tttt.asctime(tttt.localtime(tttt.time()))
time_now = tttt.strftime("%Y%m%d%H%M", tttt.localtime())
qibao_dir = os.path.dirname(a)+'/'
qi = open(qibao_dir+'qibao.txt','r')
qii = qi.readlines()
inital_time = qii[0].strip('\n')
formatt = '%Y%m%d'
today = dt.datetime.strptime(inital_time[:8],formatt)
yesterday = today - dt.timedelta(days = 1)

if int(inital_time[-4:]) <= 520:
	qibao = str(yesterday)[:4]+str(yesterday)[5:7]+str(yesterday)[8:10]+'12'
else:
	qibao = str(today)[:4]+str(today)[5:7]+str(today)[8:10]+'00'
te = str(qibao)[:4]+'-'+str(qibao)[4:6]+'-'+str(qibao)[6:8]+\
'-'+str(qibao)[8:10]
inital_time_list = pd.date_range(te,periods = 85,freq = '1h').tolist()
time_list = []
for i in range(len(inital_time_list)):
	time_list.append(str(inital_time_list[i])[:4]+str(inital_time_list[i])[5:7]+\
	str(inital_time_list[i])[8:10]+str(inital_time_list[i])[11:13])

bbbb = dt.datetime(int(qibao[:4]),int(qibao[4:6]), int(qibao[6:8]), int(qibao[8:10]))
timeaaaa = utc2local(bbbb)
qibao_local = str(timeaaaa)[:4]+str(timeaaaa)[5:7]+str(timeaaaa)[8:10]+str(timeaaaa)[11:13]

dir_f = open(absu+'predict.txt','r')
dir_ff = dir_f.readlines()
wrf_name = dir_ff[0].strip('\n')
temp_name = dir_ff[1].strip('\n')
output_name = dir_ff[2].strip('\n')
os.system('mkdir '+eval(temp_name))
os.system('mkdir '+eval(output_name)+qibao_local)
for i in range(85):
	print(str(i)+'-begin')
	aaa = str(time_list[i])
	bbb = dt.datetime(int(aaa[:4]),int(aaa[4:6]), int(aaa[6:8]), int(aaa[8:10]))
	timeaaa = utc2local(bbb)
	local = int(str(timeaaa)[:4]+str(timeaaa)[5:7]+str(timeaaa)[8:10]+str(timeaaa)[11:13])
	#print(time_list[i],local)
	clwmr =col(open_file(eval(wrf_name)+qibao+'/'+time_list[i]+'_'+'CLWMR'+'.csv'),-1)	
	lat = col(open_file(eval(wrf_name)+qibao+'/'+time_list[i]+'_'+'CLWMR'+'.csv'),-2)
	lon = col(open_file(eval(wrf_name)+qibao+'/'+time_list[i]+'_'+'CLWMR'+'.csv'),-3)
	time_wrf = col(open_file(eval(wrf_name)+qibao+'/'+time_list[i]+'_'+'CLWMR'+'.csv'),1)
	time_co = []
	for p in range(len(time_wrf)):
		time_co.append(str(time_wrf[p])[5:7]\
		+str(time_wrf[p])[8:10]+str(time_wrf[p])[11:13]+str(time_wrf[p])[14:16])
	vis = lwc(clwmr)
	
	f = open(eval(temp_name)+time_list[i]+'lwc.csv','w')
	for j in range(len(time_wrf)):	
		f.write(str(time_co[j]) + ','+str(lat[j]) + ','+str(lon[j]) + ','+ str(vis[j])+ '\n')
	f.close()
	interpolate_9_5_ccx(eval(temp_name)+time_list[i]+'lwc'+'.csv',\
	eval(temp_name)+time_list[i]+'interpolated'+'.csv')
	micpas_function_5km(eval(temp_name)+time_list[i]+'interpolated'+'.csv',\
	eval(output_name)+qibao_local+'/'+str(local)+'finish'+'.txt','0-12小时能见度客观预报lwc'\
	,time_list[i][:4],time_list[i][4:6],time_list[i][6:8],time_list[i][8:10],'1')
	print(str(i)+'-over')
print('begin:',sa)
print('over:',tttt.strftime("%Y%m%d%H%M", tttt.localtime()))
print('predict_lwc_over')
os.system('rm -r '+eval(temp_name))
























