#!/bin/bash
int=1
while(( $int<=5 ))
do
a=$(date "+%Y%m%d%H%M")
time_1=${a:8:11}
time_2=${a:10:11}
if [ $time_2 -gt 0 ] && [ $time_2 -lt 10 ]
then
	{
	python /home/user/fjfog_v1.1/0_12/0_12.py
	#python /home/user/fjfog_v1.1/0_24_obs.py
	python /home/user/fjfog_v1.1/12_72/12_72.py
	python /home/user/fjfog_v1.1/12_72_l/12_72_l.py
	python /home/user/fjfog_v1.1/12_72_l_p/12_72_l_p.py
	python /home/user/fjfog_v1.1/4_10/4_10.py
	python /home/user/fjfog_v1.1/4_10/4_10_p.py
	python /home/user/fjfog_v1.1/12_72_lwc/12_72_lwc.py
	python /home/user/fjfog_v1.1/check.py
	} &
else
	sleep 599
fi
sleep 599 
done

