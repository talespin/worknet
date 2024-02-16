#!/usr/bin/python
"""
:filename: 4.worknet_parser_one.py
:author: 최종환
:last update: 2024.01.11
 
:CHANGELOG:
    ============== ========== ====================================
    수정일            수정자        수정내용
    ============== ========== ====================================
    2024.01.11     최종환        최초생성
    ============== ========== ====================================
 
:desc:
    worknet crawl 된 html을  result 폴더에 각각 파싱하여 json 으로 변환한다.
 
"""
import os
import sys
import logging
import orjson as json
from glob import glob
from datetime import datetime
from bs4 import BeautifulSoup as bs
from multiprocessing import Pool


def parser(id:str) -> None:
    file_name = f'../crawl/{id}/{id}.html'
    logging.info(f' parse : {file_name}')
    if not os.path.exists(file_name): return
    json_file = f'../result/{id}.json'
    if os.path.exists(json_file): return
    doc = None
    result = dict(id=id)
    with open(file_name, 'rt', encoding='utf-8') as fs:
        doc = bs(fs.read(), 'html.parser')
    job_tile = doc.find('p', {'class':'tit'}).text.strip()
    result.update(dict(title=title))
    _summary = doc.find('div', {'class':'info'}).find_all('li')
    dct_summary = {}
    for dt, dd in zip(_summary.find('strong'), _summary.find('span')):
        dct_summary.update({'summary:'+dt.text.strip():dd.text.strip()})
    result.update(dct_summary)
    _jv_cont = doc.find('div', {'class':'right'}).find('div', {'class':'info'}).find_all('li')
    dct_company = {}
    for dt, dd in zip(_summary.find('strong'), _summary.find('div')):
        dct_company.update({'company:'+dt.text.strip():dd.text.strip()})
    result.update(dct_company)
    result.update({doc.find('div', {'class':'careers-table'}).find('thead').text.strip(): doc.find('div', {'class':'careers-table'}).find('tbody').text.strip()})
    _dct_careers = {}  
    ths = doc.find('div', {'class':'careers-table v1 center mt20'}).find('thead').find_all('th')
    tds = doc.find('div', {'class':'careers-table v1 center mt20'}).find('tbody').find_all('td')
    for th, td in zip(ths, tds):
        _dct_careers.update({th.text.strip():td.text.strip()})
    result.update(_dct_careers)        
    with open(json_file, 'wt') as fs:
        _ = fs.write(json.dumps(result).decode('utf-8'))


def main():
    logging.info('start parse html')
    logging.info(datetime.now())
    ids = [os.path.basename(x) for x in glob('../crawl/*')]
    pool = Pool(4)
    pool.map_async(parser, ids)
    pool.close()
    pool.join()
    logging.info('end parse html')
    logging.info(datetime.now())


if __name__=='__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    logging.root.name = 'saramin_parser_one'
    main()

