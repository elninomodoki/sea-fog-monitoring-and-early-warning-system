import sys
sys.path.append('..')
from function_time_demo import *
from math import *
import os
import csv
import os.path
import numpy as np
import pandas as pd
import os
import csv
import os.path
import math
import time as tttt
import pdb

def interpolate_station_predict_mix_function(input_name,output_name):
	def correction_ccx(lat2,lon2,lat,lon,vis):
		''' return data(m,n) '''
		data = np.zeros((len(lat2),len(lon2)))
		for k in range(len(lat)):
			m = list(lat2).index(lat[k])
			n = list(lon2).index(lon[k])
			data[m,n] = vis[k]
		return data


	def correction(lato,lono,lat,lon,vis):
		''' return lat1 lon1 vis1 '''
		allo = list(zip(lato,lono))
		all  = list(zip(lat,lon))
		print(allo[1][1])
		vis0 = []
		lon1 = []
		lat1 = []
		vis1 = []
		for ii in range(len(allo)):
			if all[ii] in allo:
				index = all.index(allo[ii])
				lat1.append(all[index][0])
				lon1.append(all[index][1])
				vis1.append(vis[index])
			else:
				lat1.append(allo[ii][0])
				lon1.append(allo[ii][1])
				vis1.append(9999.)
		return lat1,lon1,vis1

	def IDW_ccx(data,lat,lon,latt,lonn,p,v):
		'''turbo by ccx'''
		lat_l=len(lat)
		lon_l=len(lon)
		latt_l=len(latt)
		lonn_l=len(lonn)
		data_cz = np.zeros((latt_l,lonn_l))
		for ii in range(latt_l):
			for jj in range(lonn_l):
				fm=0
				fz=0
				index=0
				m=round((ii-1)*0.05/0.09)+1
				n=round((jj-1)*0.05/0.09)+1
				if m<3 and n<3 :
					for i in range(m+2):
						for j in range(n+2):
							d=sqrt((latt[ii]-lat[i])**2+(lonn[jj]-lon[j])**2)
							if (d==0):
								data_cz[ii,jj]=data[i,j]
								index=1
								break
							if d<v :
								fm=fm+1/(d**p)
								fz=fz+data[i,j]/(d**p)
						if index==1:
							break
					if (index==0):
						data_cz[ii,jj]=fz/fm
				if (m<3 and n>lon_l-2):
					for i in range(m+2):
						for j in range(n-2,lon_l):
							d=sqrt((latt[ii]-lat[i])**2+(lonn[jj]-lon[j])**2)
							if (d==0):
								data_cz[ii,jj]=data[i,j]
								index=1
								break
							if d<v :
								fm=fm+1/(d**p)
								fz=fz+data[i,j]/(d**p)
						if index==1:
							break
					if (index==0):
						data_cz[ii,jj]=fz/fm
				if (m<3 and n>2 and n<lon_l-1):
					for i in range(m+2):
						for j in range(n-2,n+2):
							d=sqrt((latt[ii]-lat[i])**2+(lonn[jj]-lon[j])**2)
							if (d==0):
								data_cz[ii,jj]=data[i,j]
								index=1
								break
							if d<v :
								fm=fm+1/(d**p)
								fz=fz+data[i,j]/(d**p)
						if index==1:
							break
					if (index==0):
						data_cz[ii,jj]=fz/fm
				if (m>lat_l-2 and n<3):
					for i in range(m-2,lat_l):
						for j in range(n+2):
							d=sqrt((latt[ii]-lat[i])**2+(lonn[jj]-lon[j])**2)
							if (d==0):
								data_cz[ii,jj]=data[i,j]
								index=1
								break
							if d<v :
								fm=fm+1/(d**p)
								fz=fz+data[i,j]/(d**p)
						if index==1:
							break
					if (index==0):
						data_cz[ii,jj]=fz/fm
				if (m>lat_l-2 and n>lon_l-2):
					for i in range(m-2,lat_l):
						for j in range(n-2,lon_l):
							d=sqrt((latt[ii]-lat[i])**2+(lonn[jj]-lon[j])**2)
							if (d==0):
								data_cz[ii,jj]=data[i,j]
								index=1
								break
							if d<v :
								fm=fm+1/(d**p)
								fz=fz+data[i,j]/(d**p)
						if index==1:
							break
					if (index==0):
						data_cz[ii,jj]=fz/fm
				if (m>lat_l-2 and n>2 and n<lon_l-1):
					for i in range(m-2,lat_l):
						for j in range(n-2,n+2):
							d=sqrt((latt[ii]-lat[i])**2+(lonn[jj]-lon[j])**2)
							if (d==0):
								data_cz[ii,jj]=data[i,j]
								index=1
								break
							if d<v :
								fm=fm+1/(d**p)
								fz=fz+data[i,j]/[d**p]
						if index==1:
							break
					if (index==0):
						data_cz[ii,jj]=fz/fm
				if (m>2 and m<lon_l-1 and n<3):
					for i in range(m-2,m+2):
						for j in range(n+2):
							d=sqrt((latt[ii]-lat[i])**2+(lonn[jj]-lon[j])**2)
							if (d==0):
								data_cz[ii,jj]=data[i,j]
								index=1
								break
							if d<v :
								fm=fm+1/(d**p)
								fz=fz+data[i,j]/(d**p)
						if index==1:
							break
					if (index==0):
						data_cz[ii,jj]=fz/fm
				if (m>2 and m<lon_l-1 and n>lon_l-2):
					for i in range(m-2,m+2):
						for j in range(n-2,lon_l):
							d=sqrt((latt[ii]-lat[i])**2+(lonn[jj]-lon[j])**2)
							if (d==0):
								data_cz[ii,jj]=data[i,j]
								index=1
								break
							if d<v :
								fm=fm+1/(d**p)
								fz=fz+data[i,j]/(d**p)
						if index==1:
							break
					if (index==0):
						data_cz[ii,jj]=fz/fm
				if (m>2 and m<lon_l-1 and n>2 and n<lon_l-1):
					for i in range(m-2,m+2):
						for j in range(n-2,n+2):
							d=sqrt((latt[ii]-lat[i])**2+(lonn[jj]-lon[j])**2)
							if (d==0):
								data_cz[ii,jj]=data[i,j]
								index=1
								break
							if d<v :
								fm=fm+1/(d**p)
								fz=fz+data[i,j]/(d**p)
						if index==1:
							break
					if (index==0):
						data_cz[ii,jj]=fz/fm
		return np.around(data_cz, decimals=4)

	def IDW(data,lat,lon,latt,lonn,p,v):
        '''IDW interpolation scheme'''
		lat_l=len(lat)
		lon_l=len(lon)
		data_cz=0.0
		fm=0.0
		fz=0.0
		index=0
		for i in range(lat_l):
			d=((latt-lat[i])**2+(lonn-lon[i])**2)**0.5
			if (d==0.0):
				data_cz=data[i]
				index=1
				break
			if (d<v and d>0 ):
				fm=fm+1/(d**p)
				fz=fz+data[i]/(d**p)
		if index == 1:
			data_cz=data[i]
		elif fm == 0 :
			data_cz=9999.
		else:
			data_cz=fz/fm
		return round(data_cz,2)
	name = os.path.dirname(__file__)
	a = os.path.abspath(name)
	absu = a+'/'
	dir_f = open(absu+'0_24_obs.txt','r')
	dir_ff = dir_f.readlines()
	obs_name = dir_ff[3].strip('\n')
	lat2 = np.around(np.arange(13,36.48,0.09),decimals = 2)
	lon2 = np.around(np.arange(107.6,131.08,0.09),decimals = 2)
	latt = np.arange(13,36.44,0.05)
	lonn = np.arange(107.6,131.04,0.05)
	lat = col(open_file(input_name),-3)
	lon = col(open_file(input_name),-2)
#	vis = col(open_file(input_name),3)
	viss1 = col(open_file(input_name),-1)
	lato = col(open_file(absu+'normal_lat_lon_9.csv'),-2)
	lono = col(open_file(absu+'normal_lat_lon_9.csv'),-3)
	lat5 = col(open_file(absu+'normal_lat_lon_5.csv'),0)
	lon5 = col(open_file(absu+'normal_lat_lon_5.csv'),1)
#	vis = correction_ccx(lat2,lon2,lat,lon,vis)
#	viss = IDW_ccx(vis,lat2,lon2,latt,lonn,2,0.1)
#	viss1 = list(viss.reshape((len(latt)**2)))


	f111 =  open(eval(obs_name)+str(input_name[-24:-16])+'00.000','r',encoding='gbk')
	f222 =  open(eval(obs_name)+str(input_name[-24:-16])+'00.000.csv','w')
	lines1 = f111.readlines()
	for line in lines1[2:]:
		line = line.replace('       ',',')
		line = line.replace('      ',',')
		line = line.replace('     ',',')
		line = line.replace('    ',',') 
		line = line.replace('   ',',')
		line = line.replace('  ',',')
		line = line.replace(' ',',')
		f222.write(line)
		#print(lines[10].replace('  ',','))
	f111.close()
	f222.close()
	
	lon_obs = col(open_file(eval(obs_name)+str(input_name[-24:-16])+'00.000.csv'),1)
	lat_obs = col(open_file(eval(obs_name)+str(input_name[-24:-16])+'00.000.csv'),2)
	vis_obs = col(open_file(eval(obs_name)+str(input_name[-24:-16])+'00.000.csv'),-9)
	lon22 = []
	lat22 = []
	vis22 = []
	for ppp in range(len(vis_obs)):
		if vis_obs[ppp] != 9999:
			lon22.append(lon_obs[ppp])
			lat22.append(lat_obs[ppp])
			vis22.append(vis_obs[ppp])
	lon3 = []
	lat3 = []
	vis3 = []
	for ii in range(len(lon5)):
		lat3.append(lat5[ii])
		lon3.append(lon5[ii])
		vis3.append(IDW(vis22,lat22,lon22,lat5[ii],lon5[ii],2,0.1))
#	f1 = open(output_name+'.csv','w')
	for j in range(len(lat3)):
		if vis3[j] != 9999.:
			viss1[j] = vis3[j]
#	for jj in range(len(lat5)):
#		f1.write(str(round(lat5[jj],2))+','+str(round(lon5[jj],2))+','+\
#		str(viss1[jj])+'\n')
#	f1.close()
	visv = np.array(viss1)
	n = int(len(lat)**0.5)
	visvv = visv.reshape(n,n)
	head = 'diamond 4'
	description = 'obs'
	years = input_name[-24:-22]
	month = input_name[-22:-20]
	day = input_name[-20:-18]
	hour = input_name[-18:-16]
	time_efficent = '0'
	level = '1'
	lon_difference = '0.05'
	lat_difference = '0.05'
	ini_lon = '107.6'
	over_lon = '131.0'
	ini_lat = '13.0'
	over_lat = '36.4'
	lat_num = str(n-1)
	lon_num = str(n-1)
	contour_difference = '100'
	ini_contour = '0'
	over_contour = '50000'
	pinghua = '1'
	jiacu = '0.0'
	f = open(output_name,'w')
	f.write('diamond 4 '+description+' '+years+' '+month+' '+day+' '+\
	hour+' '+time_efficent+' '+level+' '+lon_difference+' '+lat_difference+' '+ini_lon+' '+\
	over_lon+' '+ini_lat+' '+over_lat+' '+lat_num+' '+\
	lon_num+' '+contour_difference+' '+ini_contour+' '+over_contour+' '+pinghua+' '+jiacu+'\n')
	np.savetxt(output_name, visvv,fmt = '%.4f')
	f.close()
	
	
	
