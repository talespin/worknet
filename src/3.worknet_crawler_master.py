#!/usr/bin/python
"""
:filename: 3.worknet_crawler_master.py
:author: 최종환
:last update: 2024.01.11
 
:CHANGELOG:
    ============== ========== ====================================
    수정일            수정자        수정내용
    ============== ========== ====================================
    2024.01.11     최종환        최초생성
    ============== ========== ====================================
 
:desc:
    worknet.xlxs 을 읽어서 crawler 서버에 크롤명령어를 전송한다.
"""
import os
import sys
import logging
import pandas as pd
import orjson as json
from multiprocessing import Pool
from time import sleep


def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    display = os.environ['DISPLAY']
    items = None
    lst = []
    #items = pd.read_excel('../list/worknet_list.xlsx').to_dict('records')
    items = pd.read_csv('../list/worknet.csv').to_dict('records')
    for i, item in enumerate(items):
        id = item['id']
        if os.path.exists(f'../crawl/{id}/{id}.html'): continue
        server = (i % 7) +1
        url = item['url']
        pgm = f'rsh crawler{server} \'export DISPLAY={os.environ["DISPLAY"]};cd /mnt/work/worknet/src;/usr/share/python-3.11/bin/python 3.worknet_crawler_one.py -i {id} -u "{url}" -d "{display}"\''
        lst.append(pgm)
    print(f'total count:{len(items)},  exists count:{len(items) - len(lst)}, target count:{len(lst)}')
    print(f'crawl start')
    pool = Pool(10)
    pool.map_async(subprocess, lst)
    pool.close()
    pool.join()
    pool = None


def subprocess(pgm):
    p = os.popen(pgm)
    #sleep(40)
    print(p.read())



if __name__=='__main__':
    main()
