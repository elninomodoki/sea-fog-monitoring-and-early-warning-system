# -*- coding: utf-8 -*-
'''
Created at 20180306, revised at 20190412
@author: lxb
level prediction
20190412修改：memery usage 4×4,4threadings 100%，4min'''
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
from multiprocessing import Pool
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
	
def Normalizemaxmin(X, X_stan):
	'''normalization'''
	X_norm = np.zeros(X.shape)
	n = X.shape[1]
	xmax = np.zeros((1,n))
	xmin = np.zeros((1,n))
	xmax = np.max(X_stan,axis=0)
	xmin = np.min(X_stan,axis=0)
	for i in range(n):
		X_norm[:,i] = (X[:,i] - xmin[i])/(xmax[i] - xmin[i])
	return X_norm

print('predict_wrf_l_begin')

# record error
name = os.path.dirname(__file__)
a = os.path.abspath(name)
absu = a+'/'
fsock = open(absu+'predict_wrf_l_error.log', 'a')
#sys.stderr = fsock
sa = tttt.strftime("%Y%m%d%H%M", tttt.localtime())
ef = open(absu+'predict_wrf_l_error.log', 'a')
ef.write('*****************'+str(sa)+'*****************'+'\n')
ef.close()

# get current time
localtime = tttt.asctime(tttt.localtime(tttt.time()))
time_now = tttt.strftime("%Y%m%d%H%M", tttt.localtime())

# reading initial time from file
qibao_dir = os.path.dirname(a)+'/'
qi = open(qibao_dir+'qibao.txt','r')
qii = qi.readlines()
inital_time = qii[0].strip('\n')

# for test 
#inital_times = '2017011000'


# format initial time
formatt = '%Y%m%d'
today = dt.datetime.strptime(inital_time[:8],formatt)
yesterday = today - dt.timedelta(days = 1)

# handling time gap between model operating and transporting 
if int(inital_time[-4:]) <= 520:
	qibao = str(yesterday)[:4]+str(yesterday)[5:7]+str(yesterday)[8:10]+'12'
else:
	qibao = str(today)[:4]+str(today)[5:7]+str(today)[8:10]+'00'
te = str(qibao)[:4]+'-'+str(qibao)[4:6]+'-'+str(qibao)[6:8]+\
'-'+str(qibao)[8:10]
# generate time series
inital_time_list = pd.date_range(te,periods = 85,freq = '1h').tolist()
time_list = []
for i in range(len(inital_time_list)):
	time_list.append(str(inital_time_list[i])[:4]+str(inital_time_list[i])[5:7]+\
	str(inital_time_list[i])[8:10]+str(inital_time_list[i])[11:13])
#convert initial time to BJT
bbbb = dt.datetime(int(qibao[:4]),int(qibao[4:6]), int(qibao[6:8]), int(qibao[8:10]))
timeaaaa = utc2local(bbbb)
qibao_local = str(timeaaaa)[:4]+str(timeaaaa)[5:7]+str(timeaaaa)[8:10]+str(timeaaaa)[11:13]

# read path from file
dir_f = open(absu+'predict.txt','r')
dir_ff = dir_f.readlines()
wrf_name = dir_ff[0].strip('\n')
output_name = dir_ff[1].strip('\n')
model_name = dir_ff[2].strip('\n')
#	output_name_over = dir_ff[3].strip('\n')
vis_pool_name = dir_ff[4].strip('\n')
vis_micaps_pool_name = dir_ff[5].strip('\n')
os.system('mkdir '+eval(output_name))
#os.system('mkdir '+eval(output_name_over))
os.system('mkdir '+eval(vis_pool_name)+qibao_local)
os.system('mkdir '+eval(vis_micaps_pool_name)+qibao_local)

# prediction
def predict_wrf_l(i):
	print(str(i)+'-begin')
	aaa = str(time_list[i])
	bbb = dt.datetime(int(aaa[:4]),int(aaa[4:6]), int(aaa[6:8]), int(aaa[8:10]))
	timeaaa = utc2local(bbb)
	local = int(str(timeaaa)[:4]+str(timeaaa)[5:7]+str(timeaaa)[8:10]+str(timeaaa)[11:13])
	dataset = read_csv(eval(vis_pool_name)+qibao_local+'/'+time_list[i]+'vis_cos'+'.csv', header=None)
	# load model
	model_l = load_model(eval(model_name)+'all_level_4_256_256weights.50-0.99.hdf5')
	values = dataset.values
	values1 = values.astype('float32')
	XX = values1[:, 3:-1]
	#print(XX[1])
	where_are_nan = np.isnan(XX)
	where_are_inf = np.isinf(XX)
	XX[where_are_nan] = 0
	XX[where_are_inf] = 0
	# normalization and prediction
	x_stan = pd.read_csv(eval(model_name)+'min_max_new.csv', header = None, sep = ',').values
	X = Normalizemaxmin(values1[:,3:], x_stan)
	pred = model_l.predict_classes(X, batch_size=1024)
	pre = MaxMin_inverse(pred).reshape(len(pred),1)
	del x_stan
	f11 = open(eval(output_name)+time_list[i]+'level'+'.csv','w')	
	for p in range(len(dataset)):
		for q in range(3):
			f11.write(str(dataset[q][p])+',')
		f11.write(str(pred[p])+'\n')
	f11.close()
	# interpolation
	interpolate_9_5_ccx_level(eval(output_name)+time_list[i]+'level'+'.csv',\
	eval(output_name)+time_list[i]+'interpolated'+'.csv')
	micpas_function_5km_level(eval(output_name)+time_list[i]+'interpolated'+'.csv',\
	eval(vis_micaps_pool_name)+qibao_local+'/'+str(local)+'finish'+'.txt','12小时-3天等级精细化预报'\
	,time_list[i][:4],time_list[i][4:6],time_list[i][6:8],time_list[i][8:10],'1')
	print(str(i)+'-over')
	return 0
	
# mutithreading
pool = Pool(processes=4) 
res = pool.map(predict_wrf_l, range(85))

##test
#predict_wrf_l(0)

print('begin:',sa)
print('over:',tttt.strftime("%Y%m%d%H%M", tttt.localtime()))
print('predict_wrf_over')
os.system('rm -r '+eval(output_name))

























