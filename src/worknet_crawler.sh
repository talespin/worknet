#!/bin/bash

cd /mnt/work/worknet/src

while :
do
	python -u 1.worknet_list.py -y=yes
	python -u 3.worknet_crawler_master.py
        echo `date`
	echo "1시간 쉬었다가 다시 시작합니다."
        sleep 1h
done
