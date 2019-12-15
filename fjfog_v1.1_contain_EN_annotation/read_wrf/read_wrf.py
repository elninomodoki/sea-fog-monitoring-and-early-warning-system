# -*- coding: utf-8 -*-
'''
创建于20180306,修改于20190306
@author: lxb
读取fjwrf数据'''
import pandas as pd
import os
from time import *
import time as tttt
import datetime
import sys
import pdb

def read_24(wgrib_name,id,id2,wrf_name,dist,time_list_n,time_list_w_n):
	'''read grib after croping, output as csv'''
	os.chdir(eval(wgrib_name))
	#os.chdir('/home/ouc/')
	final_name = wrf_name + time_list_w_n[:10] + '/fjRAP_wrf_d01_' + time_list_w_n+'.grib2'
	for i in range(len(id)):
		a = './grib2/wgrib2/wgrib2 '+final_name+\
		' -ncpu 4 -match '+str(id[i])+\
		' -append'+' -csv '\
		+dist+time_list_n+'_'+str(id2[i])+'.csv'
		os.system(a)

def crop(wgrib_name,wrf_name,dist,time_list_w_n):
	'''crop grib to a small scale，output as grib2'''
	os.chdir(eval(wgrib_name))
	#os.chdir('/home/ouc/')
	grib_name = 'fjRAP_wrf_d01_' + time_list_w_n+'.grib2'
	final_name = eval(wrf_name) + time_list_w_n[:10] + '/'+grib_name
	a = './grib2/wgrib2/wgrib2 '+final_name+\
	' -small_grib 115:121 23:29 '+dist+grib_name
	print(a)
	os.system(a)
#-small_grib 10:20 -20:20

def CheckDir(path):
	'''check whether a path exsists'''
	if os.path.isdir(path):
		pass
	else:
		os.makedirs(path)

print('read_wrf_begin')

# record error
name = os.path.dirname(__file__)
a = os.path.abspath(name)
absu = a+'/'
fsock = open(absu+'read_wrf_error.log', 'a')
sys.stderr = fsock
sa = tttt.strftime("%Y%m%d%H%M", tttt.localtime())
ef = open(absu+'read_wrf_error.log', 'a')
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
#qibao = '2017042700'
##########################

# format initial time
te = str(qibao)[:4]+'-'+str(qibao)[4:6]+'-'+str(qibao)[6:8]+\
'-'+str(qibao)[8:10]
# generate time series
time_list_w = []
for i in range(85):
	time_list_w.append(qibao+'f'+'{:0>3}'.format(i))
inital_time_list = pd.date_range(te,periods = 85,freq = '1h').tolist()
time_list = []
for i in range(len(inital_time_list)):
	time_list.append(str(inital_time_list[i])[:4]+str(inital_time_list[i])[5:7]+\
	str(inital_time_list[i])[8:10]+str(inital_time_list[i])[11:13])

# read path from file
dir_f = open(absu+'read_wrf.txt','r')
dir_ff = dir_f.readlines()
wrf_name = dir_ff[0].strip('\n')
wgrib_name = dir_ff[1].strip('\n')
wrf_pool_name = dir_ff[2].strip('\n')
after_crop_dir = dir_ff[3].strip('\n')
os.system('mkdir '+eval(wrf_pool_name)+qibao)
os.system('mkdir '+eval(after_crop_dir)+qibao)
output_name = eval(wrf_pool_name)+qibao+'/'
output_name_crop = eval(after_crop_dir)+qibao+'/'


# read data
for i in range(len(time_list_w)):
	crop(wgrib_name,wrf_name,output_name_crop,time_list_w[i])
	read_24(wgrib_name,['\':DPT:2 m above ground\'','\':TMP:2 m above ground\'','\':TMP:850 mb\'','\':RH:925 mb\'','\':UGRD:10 m above ground\'','\':VGRD:10 m above ground\'',\
'\':TMP:surface\'','\':HPBL:surface\'','\':LCDC:low cloud layer\'','\':RH:2 m above ground\'','\':CLWMR:1000 mb\''],\
['DPT_2m','TMP_2m','TMP_850','RH_925','u_10','v_10','t_surface','HPBL','LCDC','RH_2m','CLWMR'],\
after_crop_dir,output_name,time_list[i],time_list_w[i])
print('begin:',sa)
print('over:',tttt.strftime("%Y%m%d%H%M", tttt.localtime()))
print('read_wrf_over')























