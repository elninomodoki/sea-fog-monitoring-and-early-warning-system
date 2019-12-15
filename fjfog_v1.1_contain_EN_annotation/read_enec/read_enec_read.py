# -*- coding: utf-8 -*-
'''
Created at 20180306, revised at 20190426
@author: lxb
read ENEC data
'''
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
import subprocess

def read_ecen(id,id2,wrf_name,dist,ec_list_ee,time_list_w):
	'''read ENEC data'''
	# grib
	os.chdir(eval(wgrib_name))
	for w in range(len(time_list_w)):
		os.system('mkdir '+ dist+time_list_w[w])
		if time_list_w[w] == ec_list_ee[34:51]:
			flag = w
			inn = 0
			break
		else:
			inn = 1
	if inn == 0:
		for jj in range(len(id2)):
			os.system('mkdir '+ dist+time_list_w[flag]+'/'+id2[jj])
			for kk in range(0,52):#(0,52)
				# handling missing values
				if len(id1[jj][kk]) < 6:
					final_name = eval(wrf_name)+qibao+'/' + ec_list_ee 
					a = './wgrib/wgrib '+final_name+' -ncpu 4'+\
					' -d '+str(id1[jj][kk]) +' -h -text -o '\
					+dist+time_list_w[flag]+'/'+id2[jj]+'/'+time_list_w[flag][:6]+'_'+time_list_w[flag][8:14]+'_'+str(id2[jj])+'_'+'{:0>2}'.format(str(kk))+'.txt'
					os.system(a)
				else:
					print('File is Not Complete %i' %(kk))



print('read_enec_begin')

# record error
name = os.path.dirname(__file__)
a = os.path.abspath(name)
absu = a+'/'
fsock = open(absu+'read_enec_error.log', 'a')
sys.stderr = fsock
sa = tttt.strftime("%Y%m%d%H%M", tttt.localtime())
ef = open(absu+'read_enec_error.log', 'a')
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
# test
#qibao = '2018031000'
##########################

# normalization initial time
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
print(len(time_list_w))


# read path from file
dir_f = open(absu+'read_enec.txt','r')
dir_ff = dir_f.readlines()
wrf_name = dir_ff[0].strip('\n')
wgrib_name = dir_ff[1].strip('\n')
wrf_pool_name = dir_ff[2].strip('\n')
os.system('mkdir '+eval(wrf_pool_name)+qibao)
os.system('mkdir '+eval(wrf_name)+'temp')
output_name = eval(wrf_pool_name)+qibao+'/'
ec_list = all_path(eval(wrf_name)+qibao)


# change to the directory of unziped, prepare for reading
os.chdir(eval(wrf_name)+qibao)

# get "door number"
for ee in range(len(ec_list)):
	os.chdir(eval(wgrib_name))                           
	# output name to file
	os.system('./wgrib/wgrib '+eval(wrf_name)+qibao+'/'+ec_list[ee]+' -v > '+eval(wrf_name)+'temp/'+ec_list[ee]+'.txt')
	id1 = []
	id1_temp = []
	#id2 = ['SSTK','10U','10V','R1000mb','2D','2T']
	id2 = ['10Usfc','10Vsfc','2Dsfc','2Tsfc','LCCsfc','SSTKsfc','R1000 mb',\
	'T850 mb','T925 mb','T1000 mb']
	id22 = ['10Usfc','10Vsfc','2Dsfc','2Tsfc','LCCsfc','SSTKsfc','R1000mb',\
	'T850mb','T925mb','T1000mb']
	fe = open(eval(wrf_name)+'temp/'+ec_list[ee]+'.txt','r')
	fee = fe.readlines()
	for i in range(len(fee)):
		fee[i] = fee[i].split(':')
	for j in range(len(id2)):
		id1_temp = []
		#465:19518913:D=2018031000:T:925 	mb:kpds=130,100,925:anl:type=Perturbed forecast 16:winds are N/S:"Temperature [K] 
		for k in range(0,52):#(0,52)
			flag_e = 0
			for i in range(len(fee)):
				if fee[i][3]+fee[i][4] == id2[j] and fee[i][7][-2:] == str(int(k)):
					id1_temp.append(fee[i][0])
					flag_e = flag_e + 1
					break
			if flag_e == 0:
				id1_temp.append('nan'+str(int(k))+'nan')
		id1.append(id1_temp)
	print(id1)
	read_ecen(id1,id22,wrf_name,output_name,ec_list[ee],time_list_w)
print('begin:',sa)
print('over:',tttt.strftime("%Y%m%d%H%M", tttt.localtime()))
print('read_enec_over')
os.system('rm -r '+eval(wrf_name)+'temp')






















