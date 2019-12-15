#encoding=utf-8
import os
import csv
import math
import time

def col(lines,lie):
	line = []
	for i in range(len(lines)):
		line.append((lines[i][lie]))
		line1 = map(eval, line)
	return list(line1)

def cole(lines,lie):
	line = []
	#print('****************',len(lines))
	for i in range(1,len(lines)):
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

def open_file_e(filename):
	with open(filename, 'r') as file_to_read:
		lines = file_to_read.readlines()
	return lines

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
		if 1010000 <= int(time[i]) < 3010000:
			sea[i] = 1
		elif 3010000 <= int(time[i]) < 6010000:
			sea[i] = 2
		elif 6010000 <= int(time[i]) < 9010000:
			sea[i] = 3
		elif 9010000 <= int(time[i]) < 12010000:
			sea[i] = 4
		else:
			sea[i] = 1
	return sea
		
def season2(time):
	sea = [0]*len(time)
	for i in range(len(time)):
		if 1010000 <= int(time[i]) < 3010000:
			sea[i] = 1
		elif 3010000 <= int(time[i]) < 5010000:
			sea[i] = 2
		elif 5010000 <= int(time[i]) < 9010000:
			sea[i] = 3
		elif 9010000 <= int(time[i]) < 12010000:
			sea[i] = 1
		else:
			sea[i] = 4
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
			
def readd(id,id2,wrf_name,dist,pre_day,time_list_n,time_list_w_n):
	os.chdir('/home/lbb/fjwrf')
	final_name = wrf_name + time_list_w_n[:10] + '/fjRAP_wrf_d01_' + time_list_w_n+'.grib2'
	for i in range(len(id)):
		a = './grib2/wgrib2/wgrib2 '+final_name+\
		' -match '+str(id[i])+\
		' -append'+' -csv '\
		+dist+time_list_n+'_'+str(id2[i])+'.csv'
		os.system(a)

def read2(id,id2,wrf_name,dist,pre_day,time_list,time_list_w):
	os.chdir('/home/lbb/fjwrf')
	for j in range(len(time_list_w)):
		for jj in range(1,46):
			final_name = wrf_name + time_list_w[j][:10] + \
			'/e'+'{:0>3}'.format(jj)+'/FJ-ENS_d01_' + time_list_w[j]+'_e'+'{:0>3}'.format(jj)+'.grib2'
			for i in range(len(id)):
				a = './grib2/wgrib2/wgrib2 '+final_name+\
				' -match '+str(id[i])+\
				' -append'+' -csv '\
				+dist+time_list[j]+'_'+'{:0>3}'.format(jj)+'_'+str(id2[i])+'.csv'
				os.system(a)
				
def read22(id,id2,wrf_name,dist,pre_day,time_list_n,time_list_w_n):
	os.chdir('/home/lbb/fjwrf')
	for jj in range(1,46):
		final_name = wrf_name + time_list_w_n[:10] + \
		'/e'+'{:0>3}'.format(jj)+'/FJ-ENS_d01_' + time_list_w_n+'_e'+'{:0>3}'.format(jj)+'.grib2'
		for i in range(len(id)):
			a = './grib2/wgrib2/wgrib2 '+final_name+\
			' -match '+str(id[i])+\
			' -append'+' -csv '\
			+dist+time_list_n+'_'+'{:0>3}'.format(jj)+'_'+str(id2[i])+'.csv'
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
 
def all_path_str(dirname):
 result = []
 for maindir, subdir, file_name_list in os.walk(dirname):
     for filename in file_name_list:
         apath = os.path.join(filename)
         result.append(apath[-6:-4])
 return result
 
def all_path_str_content(dirname):
 result = []
 for maindir, subdir, file_name_list in os.walk(dirname):
     for filename in file_name_list:
         apath = os.path.join(filename)
         #print(dirname+'/'+filename)
         #print('big',os.path.getsize(dirname+'/'+filename))
         if os.path.getsize(dirname+'/'+apath) > 1000:
             result.append(apath[-6:-4])
 #print('result:',result)
 return result

def get_time():
	a = time.strftime("%Y%m%d%H", time.localtime())
	if int(a[-2:]) < 12:
		b = a[:-2]+'00'
	else:
		b = a[:-2]+'12'
	return b

def lwc(a):
	dd = [0]*len(a)
	for i in range(len(a)):
		if a[i] == 0:
			dd[i] = 9999.
		else:
			dd[i] = 1000*0.06152*(a[i]**(-0.28))
			#print(dd[i])
	return dd

























