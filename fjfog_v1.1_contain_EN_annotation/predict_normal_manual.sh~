#!/bin/bash
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
