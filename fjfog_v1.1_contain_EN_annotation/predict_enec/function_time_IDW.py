#encoding=utf-8
import os
import csv
from math import *
import time
import numpy as np
def col(lines,lie):
	line = []
	for i in range(len(lines)):
		line.append((lines[i][lie]))
		line1 = map(eval, line)
	return list(line1)

def open_file(filename):
	with open(filename, 'r') as file_to_read:
		lines = file_to_read.readlines()
		line2 = lines
		for i in range(len(lines)):
			line2[i] = lines[i].split(',')
	return line2
	
def fsi(t_surface,dpt_2m,t_850,u_10m,v_10m):
	fsi_index = [0]*len(t_surface)
	for i in range(len(t_surface)):
		fsi_index[i] = 2*abs(t_surface[i]-dpt_2m[i])+2*abs(t_surface[i]-t_850[i])\
		+0.5*((u_10m[i]**2+v_10m[i]**2)**0.5)
	return fsi_index
	
def fsl(t_2m,dpt_2m,rh_2m):
	fsl_index = [0]*len(t_2m)
	for i in range(len(t_2m)):
		fsl_index[i] = 1609.334*6000.*(t_2m[i]-dpt_2m[i])/(rh_2m[i]**1.75)
	return fsl_index

def season(time):
	sea = [0]*len(time)
	for i in range(len(time)):
		if 1701010000 <= int(time[i]) < 1703010000:
			sea[i] = 1
		elif 1703010000 <= int(time[i]) < 1706010000:
			sea[i] = 2
		elif 1706010000 <= int(time[i]) < 1709010000:
			sea[i] = 3
		elif 1709010000 <= int(time[i]) < 1712010000:
			sea[i] = 4
		else:
			sea[i] = 1
	return sea
		
def speed(u_10m,v_10m):
	sped = [0]*len(u_10m)
	for i in range(len(u_10m)):
		if u_10m[i]!= 9999. and v_10m[i]!= 9999.:
			sped[i] = (u_10m[i]**2+v_10m[i]**2)**0.5
		else:
			sped[i] = 9999.
	return sped
	
def direction(u,v):
	pi = 3.1415926535
	dirc = [0]*len(u)
	for i in range(len(u)):
		if u[i]!= 9999. and v[i]!= 9999.:
			if (u[i]>0. and v[i]>0.): dirc[i]=270-math.atan(v[i]/u[i])*180/pi
			if (u[i]<0. and v[i]>0.): dirc[i]=90-math.atan(v[i]/u[i])*180/pi
			if (u[i]<0. and v[i]<0.): dirc[i]=90-math.atan(v[i]/u[i])*180/pi
			if (u[i]>0. and v[i]<0.): dirc[i]=270-math.atan(v[i]/u[i])*180/pi
			if (u[i]==0. and v[i]>0.): dirc[i]=180
			if (u[i]==0. and v[i]<0.): dirc[i]=0
			if (u[i]>0. and v[i]==0.): dirc[i]=270
			if (u[i]<0. and v[i]==0.): dirc[i]=90
			if (u[i]==0. and v[i]==0.): dirc[i]=9999.
		else:
			dirc[i] = 9999.
	return dirc

def ddd(t_2m,dpt_2m):
	dd = [0]*len(t_2m)
	for i in range(len(t_2m)):
		dd[i] = t_2m[i]-dpt_2m[i]
	return dd
	
def read(id,id2,wrf_name,dist,pre_day,time_list,time_list_w):
	os.chdir('/home/lbb/fjwrf')
	for j in range(len(time_list_w)):
		final_name = wrf_name + time_list_w[j][:10] + '/fjRAP_wrf_d01_' + time_list_w[j]+'.grib2'
		for i in range(len(id)):
			a = './grib2/wgrib2/wgrib2 '+final_name+\
			' -match '+str(id[i])+\
			' -append'+' -csv '\
			+dist+time_list[j]+'_'+str(id2[i])+'.csv'
			os.system(a)

def MaxMinNormalization(x):
	x = (x - 50.) / 90000.
	return x
	
def MaxMin_inverse(x):
	x = 90000.*x+50.
	return x

def traversalDir_FirstDir(path):
	list = []
	if (os.path.exists(path)):
		files = os.listdir(path)
		for file in files:
			m = os.path.join(path,file)
			if (os.path.isdir(m)):
				h = os.path.split(m)
				list.append(h[1])
	list.sort()
	return list
	
def all_path(dirname):
 result = []
 for maindir, subdir, file_name_list in os.walk(dirname):
     for filename in file_name_list:
         apath = os.path.join(filename)
         result.append(apath)
 return result

def get_time():
	a = time.strftime("%Y%m%d%H", time.localtime())
	if int(a[-2:]) < 12:
		b = a[:-2]+'00'
	else:
		b = a[:-2]+'12'
	return b

def col1(lines,lie):
	line = []
	for i in range(len(lines)):
		line.append((lines[i][lie]))
		line1 = map(eval, line)
	return list(line1)

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

def ts(yuezhi,forc,obse):
	H=0
	F=0
	M=0
	C=0
	for i in range(len(forc)):
		if(forc[i]>=yuezhi and obse[i]>=yuezhi):#正确否定
			C=C+1
		if(forc[i]>=yuezhi and obse[i]<yuezhi):#漏报
			M=M+1
		if(forc[i]<yuezhi and obse[i]>=yuezhi):#空报
			F=F+1
		if(forc[i]<yuezhi and obse[i]<yuezhi):#命中
			H=H+1
	Fo=H+F
	Ob=H+M
	N=H+F+M+C
	ets=(H-Fo*Ob/N)/(H+F+M-Fo*Ob/N)
	return ets,H,F,M,C

def correction_ccx(lat2,lon2,lat,lon,vis):
	''' return data(m,n) '''
	data = np.zeros((len(lat2),len(lon2)))
	for k in range(len(lat)):
		if (lat[k] in lat2) and (lon[k] in lon2):
			m = list(lat2).index(lat[k])
			n = list(lon2).index(lon[k])
			data[m,n] = vis[k]
	return data

#def correction_ccx(lat2,lon2,lat,lon,vis):
#	''' return data(m,n) '''
#	data = np.zeros((len(lat2),len(lon2)))
#	for k in range(len(lat)):
#		m = list(lat2).index(lat[k])
#		n = list(lon2).index(lon[k])
#		data[m,n] = vis[k]
#	return data

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
			m=round((ii-1)*0.5/1.)+1
			n=round((jj-1)*0.5/1.)+1
			#print(m,n)
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
				if (index==0) and fm != 0.:
					data_cz[ii,jj]=fz/fm
				else:
					data_cz[ii,jj]=9999.
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
				if (index==0) and fm != 0.:
					data_cz[ii,jj]=fz/fm
				else:
					data_cz[ii,jj]=9999.
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
				if (index==0) and fm != 0.:
					data_cz[ii,jj]=fz/fm
				else:
					data_cz[ii,jj]=9999.
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
				if (index==0) and fm != 0.:
					data_cz[ii,jj]=fz/fm
				else:
					data_cz[ii,jj]=9999.
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
				if (index==0) and fm != 0.:
					data_cz[ii,jj]=fz/fm
				else:
					data_cz[ii,jj]=9999.
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
				if (index==0) and fm != 0.:
					data_cz[ii,jj]=fz/fm
				else:
					data_cz[ii,jj]=9999.
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
				if (index==0) and fm != 0.:
					data_cz[ii,jj]=fz/fm
				else:
					data_cz[ii,jj]=9999.
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
				if (index==0) and fm != 0.:
					data_cz[ii,jj]=fz/fm
				else:
					data_cz[ii,jj]=9999.
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
				if (index==0) and fm != 0.:
					data_cz[ii,jj]=fz/fm
				else:
					data_cz[ii,jj]=9999.
	return np.around(data_cz, decimals=4)


















