#!/home/lbb/anaconda3/bin/python3.6
# -*- coding: utf-8 -*-
'''
Created at 2018306, revised at 20190429
@author: lxb
long-term prediction'''

#revised at 20190430，the interpolation result is saved as local time
import sys
sys.path.append('..')
#from function_time_IDW import IDW_ccx
from function_time_IDW import *
import numpy as np
np.random.seed(1337)
import h5py
import pandas as pd
import os
import csv
import os.path
import math
from time import *
from function_time_demo import *
from pandas import read_csv
import time as tttt
from scipy import interpolate
import keras
from keras.models import load_model
import sklearn
from sklearn.model_selection import train_test_split
from keras.utils import np_utils
from sklearn.preprocessing import MinMaxScaler
from micaps_function import *
import sys
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
	'''Normalization'''
	X_norm = np.zeros(X.shape)
	n = X.shape[1]
	xmax = np.zeros((1,n))
	xmin = np.zeros((1,n))
	xmax = np.max(X_stan,axis=0)
	xmin = np.min(X_stan,axis=0)
	for i in range(n):
		X_norm[:,i] = (X[:,i] - xmin[i])/(xmax[i] - xmin[i])
	return X_norm
	
print('predict_enec_begin')

# record error
name = os.path.dirname(__file__)
a = os.path.abspath(name)
absu = a+'/'
fsock = open(absu+'predict_enec_error.log', 'a')
sys.stderr = fsock
sa = tttt.strftime("%Y%m%d%H%M", tttt.localtime())
ef = open(absu+'predict_enec_error.log', 'a')
ef.write('*****************'+str(sa)+'*****************'+'\n')
ef.close()

# read initial time from file
qibao_dir = os.path.dirname(a)+'/'
qi = open(qibao_dir+'qibao.txt','r')
qii = qi.readlines()
inital_time = qii[0].strip('\n')

# format the initail time
formatt = '%Y%m%d'
today = dt.datetime.strptime(inital_time[:8],formatt)
yesterday = today - dt.timedelta(days = 1)

# the gap between model operating and transporting is 7 hours, set two key time point
if int(inital_time[-4:]) <= 510:
	qibao = str(yesterday)[:4]+str(yesterday)[5:7]+str(yesterday)[8:10]+'12'
else:
	qibao = str(today)[:4]+str(today)[5:7]+str(today)[8:10]+'00'

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
print(qibao)

#convert UTC to BJT, file saved as BJT
bbbb = dt.datetime(int(qibao[:4]),int(qibao[4:6]), int(qibao[6:8]), int(qibao[8:10]))
timeaaaa = utc2local(bbbb)
qibao_local = str(timeaaaa)[:4]+str(timeaaaa)[5:7]+str(timeaaaa)[8:10]+str(timeaaaa)[11:13]


# read path from file
dir_f = open(absu+'predict.txt','r')
dir_ff = dir_f.readlines()
output_name = dir_ff[0].strip('\n')
model_name = dir_ff[1].strip('\n')
output_name_over = dir_ff[2].strip('\n')
temp_name = dir_ff[3].strip('\n')
os.system('mkdir '+eval(temp_name))
os.system('mkdir '+eval(output_name_over)+qibao_local)


# predict per hour
def predict_enec(i):
	print(str(i)+'-begin')
	aaa = str(time_list[i])
	bbb = dt.datetime(int(aaa[:4]),int(aaa[4:6]), int(aaa[6:8]), int(aaa[8:10]))
	timeaaa = utc2local(bbb)
	local = int(str(timeaaa)[:4]+str(timeaaa)[5:7]+str(timeaaa)[8:10]+str(timeaaa)[11:13])
	# read variable, 12 and 45 represent the distribution of grids
	son_list_10Usfc = all_path_str(eval(output_name)+qibao+'/'+time_list_w[i]+'/10Usfc')#12
	son_list_10Vsfc = all_path_str(eval(output_name)+qibao+'/'+time_list_w[i]+'/10Vsfc')#12
	son_list_SSTKsfc = all_path_str(eval(output_name)+qibao+'/'+time_list_w[i]+'/SSTKsfc')#12
	son_list_2Dsfc = all_path_str(eval(output_name)+qibao+'/'+time_list_w[i]+'/2Dsfc')#12
	son_list_2Tsfc = all_path_str(eval(output_name)+qibao+'/'+time_list_w[i]+'/2Tsfc')#45
	son_list_LCCsfc = all_path_str(eval(output_name)+qibao+'/'+time_list_w[i]+'/LCCsfc')#12
	# handling the missing values
	set_1 = set(son_list_10Usfc)
	set_2 = set(son_list_10Vsfc)
	set_3 = set(son_list_LCCsfc)
	set_4 = set(son_list_2Dsfc)
	set_5 = set(son_list_2Tsfc)
	set1 = set_1&set_2
	set2 = set1&set_3
	set3 = set2&set_4
	set4 = set3&set_5
	son_list_temp = list(set4)
	son_lisr_fi =[ int(x) for x in son_list_temp]
	# raise errer if none model is selected, otherwise data reading process begins
	if len(son_lisr_fi) == 0:
		print('File Not Found')
	else:
		jjj = son_lisr_fi[0]
		u_10m =cole(open_file(eval(output_name)+qibao+'/'+time_list_w[i]+'/10Usfc/'+time_list_w[i][:6]+'_'+time_list_w[i][8:14]+'_'+'10Usfc'+'_'+'{:0>2}'.format(str(jjj))+'.txt'),0)
		v_10m=cole(open_file(eval(output_name)+qibao+'/'+time_list_w[i]+'/10Vsfc/'+time_list_w[i][:6]+'_'+time_list_w[i][8:14]+'_'+'10Vsfc'+'_'+'{:0>2}'.format(str(jjj))+'.txt'),0)
		dpt_2m =cole(open_file(eval(output_name)+qibao+'/'+time_list_w[i]+'/2Dsfc/'+time_list_w[i][:6]+'_'+time_list_w[i][8:14]+'_'+'2Dsfc'+'_'+'{:0>2}'.format(str(jjj))+'.txt'),0)
		t_2m =cole(open_file(eval(output_name)+qibao+'/'+time_list_w[i]+'/2Tsfc/'+time_list_w[i][:6]+'_'+time_list_w[i][8:14]+'_'+'2Tsfc'+'_'+'{:0>2}'.format(str(jjj))+'.txt'),0)
		lcdc0 =cole(open_file(eval(output_name)+qibao+'/'+time_list_w[i]+'/LCCsfc/'+time_list_w[i][:6]+'_'+time_list_w[i][8:14]+'_'+'LCCsfc'+'_'+'{:0>2}'.format(str(jjj))+'.txt'),0)
		lcdc = np.array(lcdc0).reshape(len(lcdc0),1)
		# interpolation 
		lat1 = np.arange(70,-10.5,-0.5)
		lon1 = np.arange(40,180.5,0.5)
		lat2 = np.arange(90,-21,-1)
		lon2 = np.arange(0,181,1)
		lata = np.arange(40,20,-0.5)
		lona = np.arange(110,130,0.5)
		latb = np.arange(40,20,-1)
		lonb = np.arange(110,130,1)
		lat11 = []
		lon11 = []
		for tt in range(len(lat1)):
			lat11 = lat11 + [lat1[tt]]*len(lon1)
			lon11 = lon11 + list(lon1)
		lat22 = []
		lon22 = []
		for tt in range(len(lat2)):
			lat22 = lat22 + [lat2[tt]]*len(lon2)
			lon22 = lon22 + list(lon2)
		lat = []
		lon = []
		for tt in range(len(lata)):
			lat = lat + [lata[tt]]*len(lona)
			lon = lon + list(lona)
		# uniform the order of lat and lon
		u_10m = correction_ccx(lata,lona,lat11,lon11,u_10m)
		v_10m = correction_ccx(lata,lona,lat11,lon11,v_10m)
		dpt_2m = correction_ccx(lata,lona,lat11,lon11,dpt_2m)
		t_2m = correction_ccx(latb,lonb,lat22,lon22,t_2m)
		lcdc = correction_ccx(lata,lona,lat11,lon11,lcdc)
		inf1= interpolate.interp2d(latb, lonb, t_2m, kind = 'linear')
		t_2m = inf1(lata, lona)
		u_10m = u_10m.reshape(len(lata)*len(lona),1)
		v_10m = v_10m.reshape(len(lata)*len(lona),1)
		dpt_2m = dpt_2m.reshape(len(lata)*len(lona),1)
		t_2m = t_2m.reshape(len(lata)*len(lona),1)
		lcdc = lcdc.reshape(len(lata)*len(lona),1)
		time_co = [time_list_w[i][8:14]+'00']*len(u_10m)
		td = t_2m - dpt_2m
		son = np.array(season(time_co)).reshape(len(time_co),1)
		time_co = np.array(time_co).reshape(len(time_co),1)
		lat = np.array(lat).astype(float).reshape(len(lat),1)
		lon = np.array(lon).astype(float).reshape(len(lon),1)
		inputdata = np.concatenate((time_co,lat,lon,son,u_10m,\
		v_10m,t_2m,dpt_2m,td,lcdc),axis = 1)
		# prediction
		model = load_model(eval(model_name)+'7_cos_100_1024_2_weights.260-0.07.hdf5')
		x_stan = pd.read_csv(eval(model_name)+'min_max_new.csv', header = None, sep = ',').values.astype('float64')
		X = Normalizemaxmin(inputdata[:,3:].astype('float64'), x_stan)
		pred = model.predict(X, batch_size=1024)
		pre = MaxMin_inverse(pred).reshape(len(pred),1)
		del x_stan
		# prepare for interpolation
		data_for_staging1 = np.concatenate((inputdata[:,:3],pre),axis = 1)
		data_fi = pd.DataFrame(data_for_staging1)
		data_fi.to_csv(eval(temp_name)+time_list[i]+'vis'+'.csv', sep = ',', header = False, index = False)
		del data_for_staging1
		del data_fi
		# interpolation
		os.chdir(absu)
		micpas_function_4_10(eval(temp_name)+time_list[i]+'vis'+'.csv',\
		eval(output_name_over)+qibao_local+'/'+str(local)+'finish'+'.txt','4-10天能见度客观预报'\
		,time_list[i][:4],time_list[i][4:6],time_list[i][6:8],time_list[i][8:10],'1')
		print(str(i)+'-over')
	return 0

#test
#predict_enec(0)

# mutithreading
pool = Pool(processes=4) 
res = pool.map(predict_enec, range(len(time_list_w)))

# log
print('begin:',sa)
print('over:',tttt.strftime("%Y%m%d%H%M", tttt.localtime()))
print('predict_enec_over')
os.system('rm '+eval(temp_name)+'*')





























