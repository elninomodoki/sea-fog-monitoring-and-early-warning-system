#data : initial data
#lat lon : lat and lon of initial
#latt lonn需要插值的经纬度
#P : parameter
#data_cz : data after interpolation
#v : effective radium
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

def interpolate_9_5_ccx(input_name,output_name):
	#print(tttt.asctime(tttt.localtime(tttt.time())))
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
		'''turbo'''
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
							#
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

	lat2 = np.around(np.arange(13,36.48,0.09),decimals = 2)
	lon2 = np.around(np.arange(107.6,131.08,0.09),decimals = 2)
	latt = np.arange(13,36.44,0.05)
	lonn = np.arange(107.6,131.04,0.05)
	lat = col(open_file(input_name),1)
	lon = col(open_file(input_name),2)
	vis = col(open_file(input_name),3)
	name = os.path.dirname(__file__)
	a = os.path.abspath(name)
	absu = a+'/'
	lato = col(open_file(absu+'2017042118_v_10.csv'),-2)
	lono = col(open_file(absu+'2017042118_v_10.csv'),-3)
	vis = correction_ccx(lat2,lon2,lat,lon,vis)
	f1 = open(output_name,'w')
	viss = IDW_ccx(vis,lat2,lon2,latt,lonn,2,0.1)
	#print(tttt.asctime(tttt.localtime(tttt.time())))
	for j in range(len(latt)):
		for jj in range(len(lonn)):
			f1.write(str(round(latt[j],2))+','+str(round(lonn[jj],2))+','+\
			str(viss[j,jj])+'\n')
	f1.close()


def interpolate_9_5_ccx_l_p(input_name,output_name):

	def col1(lines,lie):
		line = []
		for i in range(1,len(lines)):
			line.append((lines[i][lie]))
			line1 = map(eval, line)
		return list(line1)
	
	#print(tttt.asctime(tttt.localtime(tttt.time())))
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
		'''turbo'''
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
							#
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

	lat2 = np.around(np.arange(13,36.48,0.09),decimals = 2)
	lon2 = np.around(np.arange(107.6,131.08,0.09),decimals = 2)
	latt = np.arange(13,36.44,0.05)
	lonn = np.arange(107.6,131.04,0.05)
	print(input_name)
	lat = col1(open_file(input_name),0)
	lon = col1(open_file(input_name),1)
	vis1 = col1(open_file(input_name),2)
	vis2 = col1(open_file(input_name),3)
	vis3 = col1(open_file(input_name),4)
	vis4 = col1(open_file(input_name),5)
	vis5 = col1(open_file(input_name),6)
	vis6 = col1(open_file(input_name),7)
	var = [vis1,vis2,vis3,vis4,vis5,vis6]
	name = os.path.dirname(__file__)
	a = os.path.abspath(name)
	absu = a+'/'
	lato = col(open_file(absu+'2017042118_v_10.csv'),-2)
	lono = col(open_file(absu+'2017042118_v_10.csv'),-3)
	#vis = correction_ccx(lat2,lon2,lat,lon,vis)
	for u in range(1,7):
		var[u-1] = correction_ccx(lat2,lon2,lat,lon,var[u-1])
		f1 = open(output_name+str(u),'w')
		viss = IDW_ccx(var[u-1],lat2,lon2,latt,lonn,2,0.1)
		#print(tttt.asctime(tttt.localtime(tttt.time())))
		for j in range(len(latt)):
			for jj in range(len(lonn)):
				f1.write(str(round(latt[j],2))+','+str(round(lonn[jj],2))+','+\
				str(viss[j,jj])+'\n')
		f1.close()


def interpolate_9_5_ccx_level(input_name,output_name):
	#print(tttt.asctime(tttt.localtime(tttt.time())))
	def correction_ccx(lat2,lon2,lat,lon,vis):
		''' return data(m,n) '''
		data = np.zeros((len(lat2),len(lon2)))
		data[:,:] = -1
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
		'''turbo'''
		lat_l=len(lat)
		lon_l=len(lon)
		latt_l=len(latt)
		lonn_l=len(lonn)
		data_cz = np.zeros((latt_l,lonn_l))
		data_cz[:,:] = -1
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
							#
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
		return np.around(data_cz, decimals=1)

	lat2 = np.around(np.arange(13,36.48,0.09),decimals = 2)
	lon2 = np.around(np.arange(107.6,131.08,0.09),decimals = 2)
	latt = np.arange(13,36.44,0.05)
	lonn = np.arange(107.6,131.04,0.05)
	lat = col(open_file(input_name),1)
	lon = col(open_file(input_name),2)
	vis = col(open_file(input_name),3)
	#os.system('pwd')
	name = os.path.dirname(__file__)
	a = os.path.abspath(name)
	absu = a+'/'
	lato = col(open_file(absu+'2017042118_v_10.csv'),-2)
	lono = col(open_file(absu+'2017042118_v_10.csv'),-3)
	vis = correction_ccx(lat2,lon2,lat,lon,vis)
	f1 = open(output_name,'w')
	viss = IDW_ccx(vis,lat2,lon2,latt,lonn,2,0.1)
	#print(tttt.asctime(tttt.localtime(tttt.time())))
	for j in range(len(latt)):
		for jj in range(len(lonn)):
			f1.write(str(round(latt[j],2))+','+str(round(lonn[jj],2))+','+\
			str(int(viss[j,jj]))+'\n')
	f1.close()

































