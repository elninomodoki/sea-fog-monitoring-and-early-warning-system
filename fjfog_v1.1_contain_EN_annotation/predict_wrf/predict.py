# -*- coding: utf-8 -*-
'''
Creadted at 20180306, revised at 20190311
@author: lxb
read NWP output
20190313 revising：all the reading processing uses numpy and pandas, \
#run time reduces 10s，memery usage reduces 7%'''
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
#from interpolate_9_5_ccx_function_with_numpy import *
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

print('predict_wrf_begin')

# record error
name = os.path.dirname(__file__)
a = os.path.abspath(name)
absu = a+'/'
fsock = open(absu+'predict_wrf_error.log', 'a')
#sys.stderr = fsock
sa = tttt.strftime("%Y%m%d%H%M", tttt.localtime())
ef = open(absu+'predict_wrf_error.log', 'a')
ef.write('*****************'+str(sa)+'*****************'+'\n')
ef.close()

# get current time
localtime = tttt.asctime(tttt.localtime(tttt.time()))
time_now = tttt.strftime("%Y%m%d%H%M", tttt.localtime())

# read initial time from file
qibao_dir = os.path.dirname(a)+'/'
qi = open(qibao_dir+'qibao.txt','r')
qii = qi.readlines()
inital_time = qii[0].strip('\n')

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

# convert initial time to BJT
bbbb = dt.datetime(int(qibao[:4]),int(qibao[4:6]), int(qibao[6:8]), int(qibao[8:10]))
timeaaaa = utc2local(bbbb)
qibao_local = str(timeaaaa)[:4]+str(timeaaaa)[5:7]+str(timeaaaa)[8:10]+str(timeaaaa)[11:13]

# read path from file
dir_f = open(absu+'predict.txt','r')
dir_ff = dir_f.readlines()
wrf_name = dir_ff[0].strip('\n')
output_name = dir_ff[1].strip('\n')
model_name = dir_ff[2].strip('\n')
vis_pool_l_name = dir_ff[3].strip('\n')
vis_pool_name = dir_ff[4].strip('\n')
vis_micaps_pool_name = dir_ff[5].strip('\n')
os.system('mkdir '+eval(output_name))
#os.system('mkdir '+eval(output_name_over))
os.system('mkdir '+eval(vis_pool_name)+qibao_local)
os.system('mkdir '+eval(vis_micaps_pool_name)+qibao_local)
os.system('mkdir '+eval(vis_pool_l_name)+qibao_local)

# predicton
def predict_wrf(i):
	print(str(i)+'-begin')
	aaa = str(time_list[i])
	bbb = dt.datetime(int(aaa[:4]),int(aaa[4:6]), int(aaa[6:8]), int(aaa[8:10]))
	timeaaa = utc2local(bbb)
	local = int(str(timeaaa)[:4]+str(timeaaa)[5:7]+str(timeaaa)[8:10]+str(timeaaa)[11:13])
	# read variables
	lat = col(open_file(eval(wrf_name)+qibao+'/'+time_list[i]+'_'+'u_10'+'.csv'),-2)
	lon = col(open_file(eval(wrf_name)+qibao+'/'+time_list[i]+'_'+'u_10'+'.csv'),-3)
	# file name
	file_var = ['u_10','v_10','TMP_2m','DPT_2m','RH_2m','RH_925','HPBL','LCDC',\
	't_surface','TMP_850']
	# name list
	var3 = ['son','u_10m','v_10m','t_2m','dpt_2m','td','rh_2m','rh_925','hpbl','lcdc',\
	'fsi_index','fsl_index']
	inputdata = np.zeros((len(lat), len(var3)))
	tempdata = np.zeros((len(lat), 2))
	time_wrf = col(open_file(eval(wrf_name)+qibao+'/'+time_list[i]+'_'+'u_10'+'.csv'),1)
	time_co = []
	for p in range(len(time_wrf)):
		time_co.append(str(time_wrf[p])[5:7]\
		+str(time_wrf[p])[8:10]+str(time_wrf[p])[11:13]+str(time_wrf[p])[14:16])
	# calculate season index
	son = season(time_co)
	inputdata[:,var3.index('son')] = np.array(son)

	# read variables
	for name in range(4):
		file_temp = pd.read_csv(eval(wrf_name)+qibao+'/'+time_list[i]+'_'+file_var[name]+'.csv',header = None, sep=',').values
		inputdata[:,name+1] = file_temp[:,-1]
	for name in range(4,8):
		file_temp = pd.read_csv(eval(wrf_name)+qibao+'/'+time_list[i]+'_'+file_var[name]+'.csv',header = None, sep=',').values
		inputdata[:,name+2] = file_temp[:,-1]
	file_temp = pd.read_csv(eval(wrf_name)+qibao+'/'+time_list[i]+'_'+'t_surface'+'.csv',header = None, sep=',').values
	tempdata[:,0] = file_temp[:,-1]
	file_temp = pd.read_csv(eval(wrf_name)+qibao+'/'+time_list[i]+'_'+'TMP_850'+'.csv',header = None, sep=',').values
	tempdata[:,1] = file_temp[:,-1]
	del file_temp
	# calculate dew tem difference
	inputdata[:,var3.index('td')] = inputdata[:,var3.index('t_2m')]-\
	inputdata[:,var3.index('dpt_2m')]
	# fsi
	inputdata[:,var3.index('fsi_index')] = 2*abs(tempdata[:,0]-inputdata[:,var3.index('dpt_2m')])+2*abs(tempdata[:,0]-tempdata[:,1])\
		+0.5*((inputdata[:,var3.index('u_10m')]**2+inputdata[:,var3.index('v_10m')]**2)**0.5)
	# fsl
	inputdata[:,var3.index('fsl_index')] = 1609.334*6000.*(inputdata[:,var3.index('t_2m')]-inputdata[:,var3.index('dpt_2m')])/(inputdata[:,var3.index('rh_2m')]**1.75)
	time_co = np.array(time_co).astype(int).reshape(len(time_co),1)
	lat = np.array(lat).astype(float).reshape(len(lat),1)
	lon = np.array(lon).astype(float).reshape(len(lon),1)
	inputdata = np.concatenate((time_co,lat,lon,inputdata),axis = 1)
#prediction
	# model loads
	model = load_model(eval(model_name)+'12_1024_4l_1000_120-0.05.hdf5')
	# normalization and prediction
	x_stan = pd.read_csv(eval(model_name)+'min_max_new.csv', header = None, sep = ',').values
	X = Normalizemaxmin(inputdata[:,3:], x_stan)
	pred = model.predict(X, batch_size=1024)
	pre = MaxMin_inverse(pred).reshape(len(pred),1)
	del x_stan
	# preparing for interpolation
	data_for_staging1 = np.concatenate((inputdata[:,:3],pre),axis = 1)
	data_fi = pd.DataFrame(data_for_staging1)
	data_fi.to_csv(eval(vis_pool_l_name)+qibao_local+'/'+time_list[i]+'vis'+'.csv', sep = ',', header = False, index = False)
	del data_for_staging1
	del data_fi
	# perparing for fine level prediction
	data_for_staging2 = np.concatenate((inputdata[:,:],pre),axis = 1)
	low_vis_index = np.where(data_for_staging2[:,-1] < 1000)[0]
#	index = sorted(low_vis_index,key= lambda x:int(x))
#	data_for_staging3 = np.zeros((len(index), data_for_staging2.shape[1]))
#	data_for_staging3 = data_for_staging2[index,:]
	data_fi2 = pd.DataFrame(data_for_staging2[low_vis_index,:])
	data_fi2.to_csv(eval(vis_pool_l_name)+qibao_local+'/'+time_list[i]+'vis_cos'+'.csv', sep = ',', header = False, index = False)
	del data_for_staging2
	del data_fi2
	del inputdata
	del low_vis_index
	os.chdir(eval(model_name))
	# interpolation
	interpolate_9_5_ccx(eval(vis_pool_l_name)+qibao_local+'/'+time_list[i]+'vis'+'.csv',\
	eval(vis_pool_name)+qibao_local+'/'+str(local)+'interpolated'+'.csv')
	micpas_function_5km(eval(vis_pool_name)+qibao_local+'/'+str(local)+'interpolated'+'.csv',\
	eval(vis_micaps_pool_name)+qibao_local+'/'+str(local)+'finish'+'.txt','0-12小时能见度客观预报'\
	,time_list[i][:4],time_list[i][4:6],time_list[i][6:8],time_list[i][8:10],'1')
	print(str(i)+'-over')
	import gc
	gc.collect()
	return 0

# mutithreading
pool = Pool(processes=4) 
res = pool.map(predict_wrf, range(85))

##test
#predict_wrf(0)

print('begin:',sa)
print('over:',tttt.strftime("%Y%m%d%H%M", tttt.localtime()))
print('predict_wrf_over')
os.system('rm -r '+eval(output_name))




















