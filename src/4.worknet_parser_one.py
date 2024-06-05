#!/usr/bin/python
"""
:filename: 4.worknet_parser_one.py
:author: 최종환
:last update: 2024.06.04

:CHANGELOG:
    ============== ========== ====================================
    수정일            수정자        수정내용
    ============== ========== ====================================
    2024.01.11     최종환        최초생성
    2024.06.04     최종환        파싱항목변경
    ============== ========== ====================================

:desc:
    worknet crawl 파일 파싱 id 별 하나씩 파싱하여 id.json 으로 결과생성
"""
#업체명, 상세모집분야, 근무형태, 임금형태, 최소학력, 급여, 경력, 근무지역, 연관직무
#우대사항, 요구자격증, 핵심역량, 채용직급, 채용인원, 채용기업의산업

import os
import json
import pandas as pd
from glob import glob
from lxml import etree
from bs4 import BeautifulSoup as bs
import multiprocessing as mp


def get_jobkorea_채용명(doc):#*
    return doc.find('p', {'class':'title'}).text.strip()


def get_worknet_채용명(doc):#*
    return doc.find('p', {'class':'tit'}).text.strip()


def get_seoul_채용명(dom):
    return dom.xpath('//*[@id="contents"]/section/div/div[3]/div[2]/div[1]/div[1]/div[1]/p')[0].text.strip()


def get_jobkorea_업체명(doc):#*
    return doc.find('p', {'class':'name'}).text.strip()


def get_worknet_업체명(dom):#*
    try:
        return dom.xpath('//*[@id="contents"]/section/div/div[3]/div[2]/div[1]/div[2]/div[2]/ul/li[1]/div')[0].text.strip()
    except:
        return dom.xpath('//*[@id="contents"]/section/div/div[3]/div[2]/div[1]/div[2]/div[3]/ul/li[1]/div')[0].text.strip()


def get_seoul_업체명(dom):
    try:
        return dom.xpath('//*[@id="contents"]/section/div/div[3]/div[2]/div[1]/div[2]/div[2]/ul/li[1]/div')[0].text.strip()
    except:
        return dom.xpath('//*[@id="contents"]/section/div/div[3]/div[2]/div[1]/div[2]/div[3]/ul/li[1]/div')[0].text.strip()

def get_jobkorea_상세모집분야(dom):#*
    try:
        return dom.xpath('//*[@id="contents"]/div[4]/div[3]/table/tbody/tr/td[2]/text()')[0].text.strip()
    except:
        return dom.xpath("/html/body/div/div[3]/div[2]/div/section/div[4]/div[3]/table/tbody/tr/td[2]/text()")[0].strip()
    #return [x for x in str(doc.find_all('script')).split('\n') if x.find("window.dsHelper.registVal('_n_var44'")>0][0][40:-4]


def get_worknet_상세모집분야(dom):#*
    return dom.xpath('//*[@id="contents"]/section/div/div[3]/div[3]/table/tbody/tr/td')[0].text.strip()


def get_seoul_상세모집분야(dom):
    return dom.xpath('//*[@id="contents"]/section/div/div[3]/div[3]/table/tbody/tr/td')[0].text.strip()


def get_jobkorea_근무형태(doc): #*
    try:
        return doc.select("#contents > div.careers-area > div:nth-child(5) > table > tbody > tr > td:nth-child(3)")[0].text.strip()
    except:
        try:	
            return doc.select("#contents > div.careers-area > div:nth-child(5) > table > tbody > tr > td:nth-child(3)")[0].strip()
        except:
            return doc.select("#contents > div.careers-area > div:nth-child(4) > table > tbody > tr > td:nth-child(4)")[0].text.strip()


def get_worknet_근무형태(dom):
    return dom.xpath('//*[@id="contents"]/section/div/div[3]/div[2]/div[1]/div[1]/div[3]/div[1]/div/ul/li[1]/span')[0].text.strip()


def get_seoul_근무형태(dom):
    return dom.xpath('//*[@id="contents"]/section/div/div[3]/div[2]/div[1]/div[1]/div[3]/div[1]/div/ul/li[2]/span')[0].text.strip()


def get_jobkorea_임금형태(doc):
    pass


def get_worknet_임금형태(dom):
    return dom.xpath('//*[@id="contents"]/section/div/div[3]/div[2]/div[1]/div[1]/div[2]/div[2]/div/ul/li[2]/span/text()')[0].strip()


def get_seoul_임금형태(dom):
    return dom.xpath('//*[@id="contents"]/section/div/div[3]/div[2]/div[1]/div[1]/div[2]/div[2]/div/ul/li[2]/span')[0].text.strip()

	
def get_jobkorea_최소학력(dom):#*
    try:
        return dom.xpath('//*[@id="contents"]/div[4]/div[4]/table/tbody/tr/td[2]/text()')[0].text.strip()
    except:
        return dom.xpath('//*[@id="contents"]/div[4]/div[4]/table/tbody/tr/td[2]/text()')[0].strip()


def get_worknet_최소학력(dom):
    return dom.xpath('//*[@id="contents"]/section/div/div[3]/div[2]/div[1]/div[1]/div[2]/div[1]/div/ul/li[2]/span/text()')[0].strip()


def get_seoul_최소학력(dom):
    return dom.xpath('//*[@id="contents"]/section/div/div[3]/div[2]/div[1]/div[1]/div[2]/div[1]/div/ul/li[2]/span')[0].text.strip()


def get_jobkorea_급여(doc):
    pass


def get_jobkorea_경력(dom):#*
    try:
        return dom.xpath('//*[@id="contents"]/div[4]/div[4]/table/tbody/tr/td[1]/text()')[0].text.strip()
    except:
        return dom.xpath('//*[@id="contents"]/div[4]/div[4]/table/tbody/tr/td[1]/text()')[0].strip()

def get_worknet_경력(dom):#*
    try:
        return dom.xpath('//*[@id="contents"]/section/div/div[3]/div[2]/div[1]/div[1]/div[2]/div[1]/div/ul/li[1]/span/text()')[0].text.strip()
    except:
        return dom.xpath('//*[@id="contents"]/section/div/div[3]/div[4]/table/tbody/tr/td[1]/text()')[0].strip()	


def get_seoul_경력(dom):
    return dom.xpath('//*[@id="contents"]/section/div/div[3]/div[4]/table/tbody/tr/td[1]')[0].text.strip()


def get_jobkorea_근무지역(dom):#*
    try:
        return dom.xpath('//*[@id="contents"]/div[4]/div[4]/table/tbody/tr/td[5]/text()')[0].text.strip()
    except:
        try:
            return dom.xpath('//*[@id="contents"]/div[4]/div[4]/table/tbody/tr/td[5]/text()')[0].strip()
        except:
            try:
                return dom.xpath('//*[@id="contents"]/div[4]/div[3]/table/tbody/tr/td[6]')[0].text.strip()
            except:
                return dom.xpath('//*[@id="contents"]/section/div/div[3]/div[4]/table/tbody/tr/td[6]')[0].text.strip()


def get_jobkorea_연관직무(doc):
    return ''


def get_jobkorea_우대사항(doc):
    pass


def get_jobkorea_요구자격증(doc):
    pass


def get_jobkorea_핵심역량(doc):
    pass


def get_jobkorea_채용직급(doc):
    try:
        for dt, dd in zip(doc.find('div', {'class':'cont'}).find_all('dt'), doc.find('div', {'class':'cont'}).find_all('dd')):
            if dt.text.strip().find('직급') >= 0:
                return dd.text.strip()
    except:
        pass


def get_jobkorea_채용인원(dom):#*
    try:
        return dom.xpath('//*[@id="contents"]/div[4]/div[4]/table/tbody/tr/td[4]')[0].text.strip()	 
    except:
        try:
            return dom.xpath('//*[@id="contents"]/div[4]/div[4]/table/tbody/tr/td[4]')[0].strip()	 
        except:
            try:
                return dom.xpath('//*[@id="contents"]/div[4]/div[3]/table/tbody/tr/td[5]')[0].text.strip()
            except:
                return dom.xpath('//*[@id="contents"]/section/div/div[3]/div[4]/table/tbody/tr/td[4]/text()')[0].strip()


def get_jobkorea_채용기업의산업(doc):#*
    try:
        return dom.xpath('//*[@id="contents"]/div[4]/div[1]/table/tbody/tr[2]/td[1]')[0].text.strip()
    except:
        try:
            return dom.xpath('//*[@id="contents"]/div[4]/div[1]/table/tbody/tr[2]/td[1]')[0].strip()
        except:
            pass



def get_seoul_채용기업의산업(dom):
    try:
        return dom.xpath('//*[@id="contents"]/section/div/div[3]/div[2]/div[1]/div[2]/div[2]/ul/li[2]/div')[0].text.strip()
    except:
        return dom.xpath('//*[@id="contents"]/section/div/div[3]/div[2]/div[1]/div[2]/div[3]/ul/li[2]/div')[0].text.strip()	


def main(clear=False):
    crawl_list = [os.path.basename(x) for x in glob('../crawl/*')]
    os.makedirs('../parsed', exist_ok=True)
    pool = mp.Pool(5)#CPU 갯수-1 개 정도로 돌리면됩니다.
    pool.map(sub, crawl_list)
    pool.close()
    pool.close()


def sub(id):    
    json_file = f'../parsed/{id}.json'
    if os.path.exists(json_file): return
    if not os.path.exists(f'../crawl/{id}/{id}.html'): return
    with open(f'../crawl/{id}/{id}.html', 'rt', encoding='utf-8') as fs:
        doc = bs(fs.read(), 'html.parser')
        dom = etree.HTML(str(doc))
        if dom is None: return
        if len(doc.text.strip()) < 10: return
    #print(id)
    info_supply = [x for x in doc.find_all('strong') if x.text.strip() == '정보제공처'][0].parent.text.strip()
    #print('[' , info_supply.strip(), ']')
    #print(id, end=' ')
    ID = id
    채용명, 업체명, 상세모집분야, 근무형태, 임금형태, 최소학력, 급여, 경력, 근무지역, 연관직무, 우대사항, 요구자격증, 핵심역량, 채용직급, 채용인원, 채용기업의산업 = '','','','','','','','','','','','','','','',''
    if info_supply.find('서울시') >= 0:
        채용명 = get_seoul_채용명(dom)
        업체명 = get_seoul_업체명(dom)
        상세모집분야 = get_seoul_상세모집분야(dom)
        근무형태 = get_seoul_근무형태(dom)
        임금형태 = get_seoul_임금형태(dom)
        최소학력 = get_seoul_최소학력(dom)
        급여 = get_jobkorea_급여(doc)
        경력 = get_seoul_경력(dom)
        근무지역 = get_jobkorea_근무지역(dom)
        연관직무 = get_jobkorea_연관직무(dom)
        우대사항 = get_jobkorea_우대사항(doc)
        요구자격증 = get_jobkorea_요구자격증(dom)
        핵심역량 = get_jobkorea_핵심역량(dom)
        채용직급 = get_jobkorea_채용직급(doc)
        채용인원 = get_jobkorea_채용인원(dom)
        채용기업의산업 = get_seoul_채용기업의산업(dom)
    elif info_supply.find('인크루트') >= 0:
        채용명 = get_jobkorea_채용명(doc)
        업체명 = get_jobkorea_업체명(doc)
        상세모집분야 = get_jobkorea_상세모집분야(dom)
        근무형태 = get_jobkorea_근무형태(doc)
        임금형태 = get_jobkorea_임금형태(doc)
        최소학력 = get_jobkorea_최소학력(dom)
        급여 = get_jobkorea_급여(doc)
        경력 = get_jobkorea_경력(dom)
        근무지역 = get_jobkorea_근무지역(dom)
        연관직무 = get_jobkorea_연관직무(dom)
        우대사항 = get_jobkorea_우대사항(doc)
        요구자격증 = get_jobkorea_요구자격증(dom)
        핵심역량 = get_jobkorea_핵심역량(dom)
        채용직급 = get_jobkorea_채용직급(doc)
        채용인원 = get_jobkorea_채용인원(dom)
        채용기업의산업 = get_jobkorea_채용기업의산업(doc)			
    elif info_supply.find('잡코리아') >= 0:
        채용명 = get_jobkorea_채용명(doc)
        업체명 = get_jobkorea_업체명(doc)
        상세모집분야 = get_jobkorea_상세모집분야(dom)
        근무형태 = get_jobkorea_근무형태(doc)
        임금형태 = get_jobkorea_임금형태(doc)
        최소학력 = get_jobkorea_최소학력(dom)
        급여 = get_jobkorea_급여(doc)
        경력 = get_jobkorea_경력(dom)
        근무지역 = get_jobkorea_근무지역(dom)
        연관직무 = get_jobkorea_연관직무(dom)
        우대사항 = get_jobkorea_우대사항(doc)
        요구자격증 = get_jobkorea_요구자격증(dom)
        핵심역량 = get_jobkorea_핵심역량(dom)
        채용직급 = get_jobkorea_채용직급(doc)
        채용인원 = get_jobkorea_채용인원(dom)
        채용기업의산업 = get_jobkorea_채용기업의산업(doc)
    elif info_supply.find('사람인') >= 0:
        채용명 = get_jobkorea_채용명(doc)
        업체명 = get_jobkorea_업체명(doc)
        상세모집분야 = get_jobkorea_상세모집분야(dom)
        근무형태 = get_jobkorea_근무형태(doc)
        임금형태 = get_jobkorea_임금형태(doc)
        최소학력 = get_jobkorea_최소학력(dom)
        급여 = get_jobkorea_급여(doc)
        경력 = get_jobkorea_경력(dom)
        근무지역 = get_jobkorea_근무지역(dom)
        연관직무 = get_jobkorea_연관직무(dom)
        우대사항 = get_jobkorea_우대사항(doc)
        요구자격증 = get_jobkorea_요구자격증(dom)
        핵심역량 = get_jobkorea_핵심역량(dom)
        채용직급 = get_jobkorea_채용직급(doc)
        채용인원 = get_jobkorea_채용인원(dom)
        채용기업의산업 = get_jobkorea_채용기업의산업(doc)
    elif info_supply.find('워크넷') >= 0:
        채용명 = get_worknet_채용명(doc)
        업체명 = get_worknet_업체명(dom)
        상세모집분야 = get_worknet_상세모집분야(dom)
        근무형태 = get_worknet_근무형태(dom)
        임금형태 = get_worknet_임금형태(dom)
        최소학력 = get_worknet_최소학력(dom)
        급여 = get_jobkorea_급여(doc)
        경력 = get_worknet_경력(dom)
        근무지역 = get_jobkorea_근무지역(dom)
        연관직무 = get_jobkorea_연관직무(dom)
        우대사항 = get_jobkorea_우대사항(doc)
        요구자격증 = get_jobkorea_요구자격증(dom)
        핵심역량 = get_jobkorea_핵심역량(dom)
        채용직급 = get_jobkorea_채용직급(doc)
        채용인원 = get_jobkorea_채용인원(dom)
        채용기업의산업 = get_jobkorea_채용기업의산업(doc)
    data = dict(ID=ID, 채용명=채용명, 업체명=업체명, 상세모집분야=상세모집분야, 근무형태=근무형태, 임금형태=임금형태, 최소학력=최소학력, 급여=급여, 경력=경력, 근무지역=근무지역, 연관직무=연관직무, 우대사항=우대사항, 요구자격증=요구자격증, 핵심역량=핵심역량, 채용직급=채용직급, 채용인원=채용인원, 채용기업의산업=채용기업의산업)
    with open(json_file, 'wt', encoding='utf-8') as fs:
        _ = fs.write(json.dumps(data, ensure_ascii=False))	


if __name__=='__main__':
    main(True)

