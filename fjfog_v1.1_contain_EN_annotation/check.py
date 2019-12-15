import os
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
from pandas import read_csv
from sklearn.preprocessing import MinMaxScaler
import time as tttt
import datetime
import sys
import datetime as dt

def check_l(dir_name):
	def all_path(dirname):
		result = []
		for maindir, subdir, file_name_list in os.walk(dirname):
			for filename in file_name_list:
				apath = os.path.join(filename)
				result.append(apath)
		return result
	f_list = all_path(dir_name)	
	return len(f_list)

def oko(ii):
	if ii !=0:
		return 'ok'
	else:
		return 'error'
print('check_begin')
y0_12_over = oko(check_l('/home/user/fjfog_v1.1/0_12_over'))
y0_24_obs_over = oko(check_l('/home/user/fjfog_v1.1/0_24_obs_over'))
y4_10_over = oko(check_l('/home/user/fjfog_v1.1/4_10_over'))
y4_10_p_over = oko(check_l('/home/user/fjfog_v1.1/4_10_p_over'))
y12_72_l_over = oko(check_l('/home/user/fjfog_v1.1/12_72_l_over'))
y12_72_l_p_over = oko(check_l('/home/user/fjfog_v1.1/12_72_l_p_over'))
y12_72_lwc_over = oko(check_l('/home/user/fjfog_v1.1/12_72_lwc_over'))
y12_72_over = oko(check_l('/home/user/fjfog_v1.1/12_72_over'))


name = os.path.dirname(__file__)
a = os.path.abspath(name)
absu = a+'/'
sa = tttt.strftime("%Y%m%d%H%M", tttt.localtime())
ef = open(absu+'check.log', 'a')
ef.write('\n')
ef.write('*****************'+str(sa)+'*****************'+'\n')
ef.write('0_12:'+str(y0_12_over)+'\n')
ef.write('0_24_obs:'+str(y0_24_obs_over)+'\n')
ef.write('4_10:'+str(y4_10_over)+'\n')
ef.write('4_10_p:'+str(y4_10_p_over)+'\n')
ef.write('12_72_l:'+str(y12_72_l_over)+'\n')
ef.write('12_72_l_p:'+str(y12_72_l_p_over)+'\n')
ef.write('12_72_lwc:'+str(y12_72_lwc_over)+'\n')
ef.write('12_72:'+str(y12_72_over)+'\n')
ef.close()


print('check_over')

