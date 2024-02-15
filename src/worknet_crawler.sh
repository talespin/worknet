#!/bin/bash

cd /mnt/work/worknet/src

while :
do
	python 1.worknet_list.py -y=yes;python 3.worknet_crawler_master.py
        sleep 1h
done
