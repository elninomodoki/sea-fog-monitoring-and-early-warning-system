import os
import csv
import os.path
import numpy as np
from function_time_demo import *
import pandas as pd
import os
import csv
import os.path
import math
import time as tttt
from math import *
def micpas_function_5km(input_name,output_name,descri,y,m,d,h,t):
	lat = col(open_file(input_name),0)
	lon = col(open_file(input_name),1)
	vis = col(open_file(input_name),2)
	n = int(len(lat)**0.5)
	print(n)
	visv = np.array(vis)
	visvv = visv.reshape(n,n)

	head = 'diamond 4'
	description = descri
	years = y
	month = m
	day = d
	hour = h
	time_efficent = t
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
	
def micpas_function_5km_level(input_name,output_name,descri,y,m,d,h,t):
	lat = col(open_file(input_name),0)
	lon = col(open_file(input_name),1)
	vis = col(open_file(input_name),2)
	n = int(len(lat)**0.5)
	print(n)
	visv = np.array(vis)
	visvv = visv.reshape(n,n)

	head = 'diamond 4'
	description = descri
	years = y
	month = m
	day = d
	hour = h
	time_efficent = t
	level = '1'
	lon_difference = '0.05'
	lat_difference = '0.05'
	ini_lon = '107.6'
	over_lon = '131.0'
	ini_lat = '13.0'
	over_lat = '36.4'
	lat_num = str(n-1)
	lon_num = str(n-1)
	contour_difference = '1'
	ini_contour = '-1'
	over_contour = '5'
	pinghua = '1'
	jiacu = '0.0'
	f = open(output_name,'w')
	f.write('diamond 4 '+description+' '+years+' '+month+' '+day+' '+\
	hour+' '+time_efficent+' '+level+' '+lon_difference+' '+lat_difference+' '+ini_lon+' '+\
	over_lon+' '+ini_lat+' '+over_lat+' '+lat_num+' '+\
	lon_num+' '+contour_difference+' '+ini_contour+' '+over_contour+' '+pinghua+' '+jiacu+'\n')
	np.savetxt(output_name, visvv,fmt = '%.1f')
	f.close()

def micpas_function_4_10(input_name,output_name,descri,y,m,d,h,t):
	lat = col(open_file(input_name),-3)
	lon = col(open_file(input_name),-2)
	vis = col(open_file(input_name),-1)
	n = int(len(lat)**0.5)
	print(n)
	visv = np.array(vis)
	visvv = visv.reshape(n,n)

	head = 'diamond 4'
	description = descri
	years = y
	month = m
	day = d
	hour = h
	time_efficent = '1'
	level = '1'
	lon_difference = '0.5'
	lat_difference = '0.5'
	ini_lon = '110.0'
	over_lon = '130.0'
	ini_lat = '20.0'
	over_lat = '40.0'
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


def micpas_function_5km_l_p(input_name,output_name,descri,y,m,d,h,t):

	


	for u in range(1,7):
		lat = col(open_file(input_name+str(u)),0)
		lon = col(open_file(input_name+str(u)),1)
		vis1 = col(open_file(input_name+str(u)),2)
		vis2 = col(open_file(input_name+str(u)),2)
		vis3 = col(open_file(input_name+str(u)),2)
		vis4 = col(open_file(input_name+str(u)),2)
		vis5 = col(open_file(input_name+str(u)),2)
		vis6 = col(open_file(input_name+str(u)),2)
		var = [vis1,vis2,vis3,vis4,vis5,vis6]
		n = int(len(lat)**0.5)
		print(n)
		head = 'diamond 4'
		description = descri+'_'+'等级'+str(u)
		years = y
		month = m
		day = d
		hour = h
		time_efficent = t
		level = '1'
		lon_difference = '0.05'
		lat_difference = '0.05'
		ini_lon = '107.6'
		over_lon = '131.0'
		ini_lat = '13.0'
		over_lat = '36.4'
		lat_num = str(n-1)
		lon_num = str(n-1)
		contour_difference = '0.1'
		ini_contour = '0'
		over_contour = '1'
		pinghua = '1'
		jiacu = '0.0'
		visv = np.array(var[u-1])
		visvv = visv.reshape(n,n)
		f = open(output_name+str(u),'w')
		f.write('diamond 4 '+description+' '+years+' '+month+' '+day+' '+\
		hour+' '+time_efficent+' '+level+' '+lon_difference+' '+lat_difference+' '+ini_lon+' '+\
		over_lon+' '+ini_lat+' '+over_lat+' '+lat_num+' '+\
		lon_num+' '+contour_difference+' '+ini_contour+' '+over_contour+' '+pinghua+' '+jiacu+'\n')
		np.savetxt(output_name+str(u), visvv,fmt = '%.4f')
		f.close()

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

def micpas_function_4_10_2(input_name,output_name,descri,y,m,d,h,t):
	lat = col(open_file(input_name),-3)
	lon = col(open_file(input_name),-2)
	vis = col(open_file(input_name),-1)
	#print(len(lata)
	if len(lat)<1600:
		vis = vis + [-1]*(1600-len(lat))
#	print(lat[-10:])
#	print(lon[-10:])
#	print(vis[-10:])
#	print(len(lat))
#	print(len(lon))
#	print(len(vis))
#	n = int(len(lat)**0.5)
#	print(n)
	n = 40
	visv = np.array(vis)
	visvv = visv.reshape(n,n)

	head = 'diamond 4'
	description = descri
	years = y
	month = m
	day = d
	hour = h
	time_efficent = '1'
	level = '1'
	lon_difference = '0.5'
	lat_difference = '0.5'
	ini_lon = '110.0'
	over_lon = '130.0'
	ini_lat = '20.0'
	over_lat = '40.0'
	lat_num = str(n-1)
	lon_num = str(n-1)
	contour_difference = '0.1'
	ini_contour = '0'
	over_contour = '1'
	pinghua = '1'
	jiacu = '0.0'
	f = open(output_name,'w')
	f.write('diamond 4 '+description+' '+years+' '+month+' '+day+' '+\
	hour+' '+time_efficent+' '+level+' '+lon_difference+' '+lat_difference+' '+ini_lon+' '+\
	over_lon+' '+ini_lat+' '+over_lat+' '+lat_num+' '+\
	lon_num+' '+contour_difference+' '+ini_contour+' '+over_contour+' '+pinghua+' '+jiacu+'\n')
	np.savetxt(output_name, visvv,fmt = '%.4f')
	f.close()



















