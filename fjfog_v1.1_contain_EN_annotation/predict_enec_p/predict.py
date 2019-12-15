# -*- coding: utf-8 -*-
'''
Created at 20180306, revised at 20190429
@author: lxb
long-term probabilistic prediction'''
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
#import keras
#from keras.models import load_model
import sklearn
from sklearn.model_selection import train_test_split
from keras.utils import np_utils
from sklearn.preprocessing import MinMaxScaler
from micaps_function import micpas_function_4_10_2
import sys
import datetime as dt
from multiprocessing import Pool

def std(t_2m,SST):
	dd = [0]*len(t_2m)
	for i in range(len(t_2m)):
		dd[i] = SST[i]-t_2m[i]
	return dd
	
def local2utc(local_st):
	'''convert local time to UTC'''
	time_struct = tttt.mktime(local_st.timetuple())
	utc_st = dt.datetime.utcfromtimestamp(time_struct)
	return utc_st
def utc2local(utc_st):
	'''convert UTC to local'''
	now_stamp = tttt.time()
	local_time = dt.datetime.fromtimestamp(now_stamp)
	utc_time = dt.datetime.utcfromtimestamp(now_stamp)
	offset = local_time - utc_time
	local_st = utc_st + offset
	return local_st
	
print('predict_enec_p_begin')

# record error
name = os.path.dirname(__file__)
a = os.path.abspath(name)
absu = a+'/'
fsock = open(absu+'predict_enec_p_error.log', 'a')
sys.stderr = fsock
sa = tttt.strftime("%Y%m%d%H%M", tttt.localtime())
ef = open(absu+'predict_enec_p_error.log', 'a')
ef.write('*****************'+str(sa)+'*****************'+'\n')
ef.close()

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
if int(inital_time[-4:]) <= 510:
	qibao = str(yesterday)[:4]+str(yesterday)[5:7]+str(yesterday)[8:10]+'12'
else:
	qibao = str(today)[:4]+str(today)[5:7]+str(today)[8:10]+'00'
	

te = str(qibao)[:4]+'-'+str(qibao)[4:6]+'-'+str(qibao)[6:8]+\
'-'+str(qibao)[8:10]

# generate standard time series
inital_time_list = pd.date_range(te,periods = 40,freq = '6h').tolist()
time_list = []
for i in range(len(inital_time_list)):
	time_list.append(str(inital_time_list[i])[:4]+str(inital_time_list[i])[5:7]+\
	str(inital_time_list[i])[8:10]+str(inital_time_list[i])[11:13])

# convert UTC to BJT
bbbb = dt.datetime(int(qibao[:4]),int(qibao[4:6]), int(qibao[6:8]), int(qibao[8:10]))
timeaaaa = utc2local(bbbb)
qibao_local = str(timeaaaa)[:4]+str(timeaaaa)[5:7]+str(timeaaaa)[8:10]+str(timeaaaa)[11:13]
time_list_w = []
for i in range(len(time_list)):
	time_list_w.append(qibao[4:]+'00'+time_list[i][4:]+'001')

# read path from file
dir_f = open(absu+'predict.txt','r')
dir_ff = dir_f.readlines()
output_name = dir_ff[0].strip('\n')
model_name = dir_ff[1].strip('\n')
output_name_over = dir_ff[2].strip('\n')
temp_name = dir_ff[3].strip('\n')
os.system('mkdir '+eval(temp_name))
os.system('mkdir '+eval(output_name_over)+qibao_local)

# prediction
def predict_enec_p(i):
	print(str(i)+'-begin')
	# convert UTC to BJT
	aaa = str(time_list[i])
	bbb = dt.datetime(int(aaa[:4]),int(aaa[4:6]), int(aaa[6:8]), int(aaa[8:10]))
	timeaaa = utc2local(bbb)
	local = int(str(timeaaa)[:4]+str(timeaaa)[5:7]+str(timeaaa)[8:10]+str(timeaaa)[11:13])
	summ = 0.
	pro = [0. for n in range(2000)]
	# read variable, 12 and 45 represent the distribution of grids
	son_list_10Usfc = all_path_str_content(eval(output_name)+qibao+'/'+time_list_w[i]+'/10Usfc')#12
	son_list_10Vsfc = all_path_str_content(eval(output_name)+qibao+'/'+time_list_w[i]+'/10Vsfc')#12
	son_list_SSTKsfc = all_path_str_content(eval(output_name)+qibao+'/'+time_list_w[i]+'/SSTKsfc')#12
	son_list_R1000mb = all_path_str_content(eval(output_name)+qibao+'/'+time_list_w[i]+'/R1000mb')#45
	son_list_2Dsfc = all_path_str_content(eval(output_name)+qibao+'/'+time_list_w[i]+'/2Dsfc')#12
	son_list_2Tsfc = all_path_str_content(eval(output_name)+qibao+'/'+time_list_w[i]+'/2Tsfc')#45#12!!!
	# handling missing values
	set_1 = set(son_list_10Usfc)
	set_2 = set(son_list_10Vsfc)
	set_3 = set(son_list_SSTKsfc)
	set_4 = set(son_list_R1000mb)
	set_5 = set(son_list_2Dsfc)
	set_6 = set(son_list_2Tsfc)
	set1 = set_1&set_2
	set2 = set1&set_3
	set3 = set2&set_4
	set4 = set3&set_5
	set5 = set4&set_6
	son_list_temp = list(set5)
	son_lisr_fi =[ int(x) for x in son_list_temp]
	for jjj in son_lisr_fi:
		# read variables
		u_10m =cole(open_file(eval(output_name)+qibao+'/'+time_list_w[i]+'/10Usfc/'+time_list_w[i][:6]+'_'+time_list_w[i][8:14]+'_'+'10Usfc'+'_'+str(jjj)+'.txt'),0)
		v_10m=cole(open_file(eval(output_name)+qibao+'/'+time_list_w[i]+'/10Vsfc/'+time_list_w[i][:6]+'_'+time_list_w[i][8:14]+'_'+'10Vsfc'+'_'+str(jjj)+'.txt'),0)
		dpt_2m =cole(open_file(eval(output_name)+qibao+'/'+time_list_w[i]+'/2Dsfc/'+time_list_w[i][:6]+'_'+time_list_w[i][8:14]+'_'+'2Dsfc'+'_'+str(jjj)+'.txt'),0)
		t_2m =cole(open_file(eval(output_name)+qibao+'/'+time_list_w[i]+'/2Tsfc/'+time_list_w[i][:6]+'_'+time_list_w[i][8:14]+'_'+'2Tsfc'+'_'+str(jjj)+'.txt'),0)
		SST =cole(open_file(eval(output_name)+qibao+'/'+time_list_w[i]+'/SSTKsfc/'+time_list_w[i][:6]+'_'+time_list_w[i][8:14]+'_'+'SSTKsfc'+'_'+str(jjj)+'.txt'),0)
		rh_2m =cole(open_file(eval(output_name)+qibao+'/'+time_list_w[i]+'/R1000mb/'+time_list_w[i][:6]+'_'+time_list_w[i][8:14]+'_'+'R1000mb'+'_'+str(jjj)+'.txt'),0)
		t_850 =cole(open_file(eval(output_name)+qibao+'/'+time_list_w[i]+'/T850mb/'+time_list_w[i][:6]+'_'+time_list_w[i][8:14]+'_'+'T850mb'+'_'+str(jjj)+'.txt'),0)
		t_925 =cole(open_file(eval(output_name)+qibao+'/'+time_list_w[i]+'/T925mb/'+time_list_w[i][:6]+'_'+time_list_w[i][8:14]+'_'+'T925mb'+'_'+str(jjj)+'.txt'),0)
		t_1000 =cole(open_file(eval(output_name)+qibao+'/'+time_list_w[i]+'/T1000mb/'+time_list_w[i][:6]+'_'+time_list_w[i][8:14]+'_'+'T1000mb'+'_'+str(jjj)+'.txt'),0)
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
		u_10m = correction_ccx_co(lata,lona,lat11,lon11,u_10m)
		v_10m = correction_ccx_co(lata,lona,lat11,lon11,v_10m)
		dpt_2m = correction_ccx_co(lata,lona,lat11,lon11,dpt_2m)
		SST = correction_ccx_co(lata,lona,lat11,lon11,SST)
		t_2m = correction_ccx_co(lata,lona,lat11,lon11,t_2m)
		rh_2m = correction_ccx_co(latb,lonb,lat22,lon22,rh_2m)
		t_850 = correction_ccx_co(latb,lonb,lat22,lon22,t_850)
		t_925 = correction_ccx_co(latb,lonb,lat22,lon22,t_925)
		t_1000 = correction_ccx_co(latb,lonb,lat22,lon22,t_1000)
		inf1= interpolate.interp2d(latb, lonb, rh_2m, kind = 'linear')
		t_2m = inf1(lata, lona)
		rh_2m = inf1(lata, lona)
		t_850 = inf1(lata, lona)
		t_925 = inf1(lata, lona)
		t_1000 = inf1(lata, lona)
		u_10m = list(u_10m.reshape((len(lata)*len(lona))))
		v_10m = list(v_10m.reshape((len(lata)*len(lona))))
		dpt_2m = list(dpt_2m.reshape((len(lata)*len(lona))))
		SST = list(SST.reshape((len(lata)*len(lona))))
		t_2m = list(t_2m.reshape((len(lata)*len(lona))))
		rh_2m = list(rh_2m.reshape((len(lata)*len(lona))))
		t_850 = list(t_850.reshape((len(lata)*len(lona))))
		t_925 = list(t_925.reshape((len(lata)*len(lona))))
		t_1000 = list(t_1000.reshape((len(lata)*len(lona))))
		# calculate some indexs
		time_co = [time_list_w[i][8:14]+'00']*len(u_10m)
		son = season2(time_co)
		td0 = ddd(t_2m,dpt_2m)
		std0 = std(t_2m,SST)
		wind_sp0 = speed(u_10m,v_10m)
		dirc0 = direction(u_10m,v_10m)
		fsi_index0 = fsi(t_1000,dpt_2m,t_850,u_10m,v_10m)	
		fsl_index0 = fsl(t_2m,dpt_2m,rh_2m)
		latt = []
		lonn = []
		sonn = []
		td = []
		wind_sp = []
		dirc = []
		fsi_index = []
		fsl_index = []
		stdd = []
		for j in range(len(lat)):
			latt.append(lat[j])
			lonn.append(lon[j])
			sonn.append(son[j])
			td.append(td0[j])
			stdd.append(std0[j])
			wind_sp.append(wind_sp0[j])
			dirc.append(dirc0[j])
			fsi_index.append(fsi_index0[j])
			fsl_index.append(fsl_index0[j])
		# prediction basing on threshold
		for j in range(len(latt)):
			if sonn[j] == 1 or sonn[j] == 4:
				s = 0.
				if td[j] < 0.7001:
					s = s+1
				if dirc[j] < 104.1:
					s = s+1
				if wind_sp[j] < 2.:
					s = s+1
				if rh_2m[j] > 96.4:
					s = s+1
				if -2.5 <stdd[j] < 3.1:
					s = s+1
				proba = round(s/5,2)
			elif sonn[j] == 2:
				s = 0.
				if td[j] < 1.0065:
					s = s+1
				if wind_sp[j] < 2.:
					s = s+1
				if rh_2m[j] > 97.7:
					s = s+1
				if -2.5 <stdd[j] < 3.1:
					s = s+1
				proba = round(s/4,2)	
			elif sonn[j] == 3:
				s = 0.
				if td[j] < 1.1364:
					s = s+1
				if 148 < dirc[j] < 237:
					s = s+1
				if wind_sp[j] < 3.:
					s = s+1
				if rh_2m[j] > 95.9:
					s = s+1
				if -2.5 <stdd[j] < 3.1:
					s = s+1
				proba = round(s/5,2)	
			else:
				proba = 9999.
			pro[j] = pro[j]+proba
	proo = [round(pro[n]/len(son_lisr_fi),2) for n in range(len(pro))]
	f = open(eval(temp_name)+time_list[i]+'_'+'pro.csv','w')
	lata = np.arange(40,20,-0.5)
	lona = np.arange(110,130,0.5)
	lat = []
	lon = []
	for tt in range(len(lata)):
		lat = lat + [lata[tt]]*len(lona)
		lon = lon + list(lona)
	for rr in range(len(lat)):
		f.write(str(lat[rr]) + ','+str(lon[rr]) + ','+ str(proo[rr])+ '\n')
	f.close()
	os.chdir(eval(model_name))
	# interpolation
	micpas_function_4_10_2(eval(temp_name)+time_list[i]+'_pro'+'.csv',eval(output_name_over)+qibao_local+'/'+str(local)+'finish'+'.txt','4-10天能见度概率预报',str(local)[:4],str(local)[4:6],str(local)[6:8],str(local)[8:10],'1')

	print(str(i)+'-over')
	return 0

#test
#predict_enec_p(0)

# mutithreading
pool = Pool(processes=4) 
res = pool.map(predict_enec_p, range(len(time_list_w)))

print('begin:',sa)
print('over:',tttt.strftime("%Y%m%d%H%M", tttt.localtime()))
print('predict_enec_p_over')
os.system('rm -r '+eval(temp_name))





























