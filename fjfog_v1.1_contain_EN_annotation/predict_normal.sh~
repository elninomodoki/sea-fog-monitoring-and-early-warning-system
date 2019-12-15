#!/bin/bash
int=1
while(( $int<=5 ))
do
a=$(date "+%Y%m%d%H%M")
time_1=${a:8:11}
#time_2=${a:10:11}
echo $time_1
if [ $time_1 -gt 500 ] && [ $time_1 -lt 510 ]
then
b=$(date "+%Y%m%d%H%M")
echo $b > qibao.txt
	{
	python /home/user/fjfog_v1.1/read_wrf/read_wrf.py
	python /home/user/fjfog_v1.1/predict_wrf/predict.py
	python /home/user/fjfog_v1.1/predict_wrf_l/predict.py & 
	python /home/user/fjfog_v1.1/predict_lwc/predict.py
	} &
	
	
	{
	python /home/user/fjfog_v1.1/read_fjec/read_fjec.py
	python /home/user/fjfog_v1.1/predict_fjec_l_p/predict.py 
	} &
	
	{
	python /home/user/fjfog_v1.1/read_enec/read_enec_unpack.py
	python /home/user/fjfog_v1.1/read_enec/read_enec_read.py
	python /home/user/fjfog_v1.1/predict_enec/predict.py
	python /home/user/fjfog_v1.1/predict_enec_p/predict.py
	}
elif [ $time_1 -gt 1700 ] && [ $time_1 -lt 1710 ]
then
b=$(date "+%Y%m%d%H%M")
echo $b > qibao.txt

	{
	python /home/user/fjfog_v1.1/read_wrf/read_wrf.py
	python /home/user/fjfog_v1.1/predict_wrf/predict.py
	python /home/user/fjfog_v1.1/predict_wrf_l/predict.py & 
	python /home/user/fjfog_v1.1/predict_lwc/predict.py
	} &
	
	
	{
	python /home/user/fjfog_v1.1/read_fjec/read_fjec.py
	python /home/user/fjfog_v1.1/predict_fjec_l_p/predict.py 
	} &
	
	{
	python /home/user/fjfog_v1.1/read_enec/read_enec_unpack.py
	python /home/user/fjfog_v1.1/read_enec/read_enec_read.py
	python /home/user/fjfog_v1.1/predict_enec/predict.py
	python /home/user/fjfog_v1.1/predict_enec_p/predict.py
	}
else
	sleep 599
	continue
fi
sleep 36000
done
