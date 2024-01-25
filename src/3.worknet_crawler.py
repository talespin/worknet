#!/usr/bin/python
"""
:filename: 3.worknet_crawler.py
:author: 최종환
:last update: 2024.01.20
 
:CHANGELOG:
    ============== ========== ====================================
    수정일            수정자        수정내용
    ============== ========== ====================================
    2024.01.20     최종환        최초생성
    ============== ========== ====================================
 
:desc:
    워크넷 site 의 전체 지역 체용정보 목록을 이용하여 사이트 크롤
 
"""
import os
import sys
import math
import logging
import argparse
import pandas as pd
import requests as req
from time import sleep
from datetime import datetime
from bs4 import BeautifulSoup as bs


def worknet_crawler(list_file:str, overwrite:bool = False):
    if not os.path.exists(list_file):
        print('File not found:' + os.path.abspath(list_file))
        return
    with open(list_file, 'rt', encoding='utf-8') as fs:
        items = pd.read_json(fs.read()).to_dict('records')
    logging.info('worknet crawl list start:' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    base_url = 'https://www.work.go.kr'
    cookies = {
        'myRegionCdNm': '11000_%EC%84%9C%EC%9A%B8',
        'PCID': '16463621575612540009809',
        'ccguid': '17f53444a56-2ce8cbb4400aae1e9',
        'WMONID': 'g54s4U7aCMR',
        'ccsession': '18d26e8d5da-2ce8cbf8b003392bd',
        'WORKNETSESSIONID': 'lzAm6NXYIMz5BHRyPHBTvGE5Zz7f9N6EhcIzeiK5KSqpxaaoM06b!-1968499696!-2131970884',
        'NEW_MAIN_TAB_INDEX': '0',
        'SESSION_CREATION_TIME': '1705754809816',
        'isOffer': 'Y',
        'sortField': 'DATE',
        'sortOrderBy': 'DESC',
        'resultCnt': '1000',
        'hisListView': 'DTL',
    }
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        # 'Cookie': 'myRegionCdNm=11000_%EC%84%9C%EC%9A%B8; PCID=16463621575612540009809; ccguid=17f53444a56-2ce8cbb4400aae1e9; WMONID=g54s4U7aCMR; ccsession=18d26e8d5da-2ce8cbf8b003392bd; WORKNETSESSIONID=lzAm6NXYIMz5BHRyPHBTvGE5Zz7f9N6EhcIzeiK5KSqpxaaoM06b!-1968499696!-2131970884; NEW_MAIN_TAB_INDEX=0; SESSION_CREATION_TIME=1705754809816; isOffer=Y; sortField=DATE; sortOrderBy=DESC; resultCnt=10; hisListView=DTL',
        'Referer': 'https://www.work.go.kr/empInfo/empInfoSrch/list/dtlEmpSrchList.do?careerTo=&keywordJobCd=&occupation=&templateInfo=&shsyWorkSecd=&rot2WorkYn=&payGbn=&resultCnt=10&keywordJobCont=&cert=&cloDateStdt=&moreCon=&minPay=&codeDepth2Info=11000&isChkLocCall=&sortFieldInfo=DATE&major=&resrDutyExcYn=&eodwYn=&sortField=DATE&staArea=&sortOrderBy=DESC&keyword=&termSearchGbn=all&carrEssYns=&benefitSrchAndOr=O&disableEmpHopeGbn=&webIsOut=region&actServExcYn=&maxPay=&keywordStaAreaNm=&emailApplyYn=&listCookieInfo=DTL&pageCode=&codeDepth1Info=11000&keywordEtcYn=&publDutyExcYn=&keywordJobCdSeqNo=&exJobsCd=&templateDepthNmInfo=&computerPreferential=&regDateStdt=&employGbn=&empTpGbcd=&region=&infaYn=&resultCntInfo=10&siteClcd=all&cloDateEndt=&sortOrderByInfo=DESC&currntPageNo=1&indArea=&careerTypes=&searchOn=Y&tlmgYn=&subEmpHopeYn=&academicGbn=&templateDepthNoInfo=&foriegn=&mealOfferClcd=&station=&moerButtonYn=&holidayGbn=&srcKeyword=&enterPriseGbn=all&academicGbnoEdu=noEdu&cloTermSearchGbn=all&keywordWantedTitle=&stationNm=&benefitGbn=&keywordFlag=&notSrcKeyword=&essCertChk=&isEmptyHeader=&depth2SelCode=&_csrf=847af1b2-e7bf-4b52-a903-e69695122a91&keywordBusiNm=&preferentialGbn=&rot3WorkYn=&pfMatterPreferential=&regDateEndt=&staAreaLineInfo1=11000&staAreaLineInfo2=1&pageIndex=1&termContractMmcnt=&careerFrom=&laborHrShortYn=',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    os.makedirs('../crawl', exist_ok=True)
    for i, item in enumerate(items):
        logging.info(f"    crawl : {item['id']} ")
        file_name = f"../crawl/{item['id']}.html"
        if os.path.exists(file_name) and overwrite==False:
            print("    skip file")
            continue 
        sleep(5)    
        res = req.get(item['url'], headers=headers)
        with open(file_name, 'wb') as fs:
            fs.write(res.content)
    logging.info('worknet crawl list end:' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


if __name__=='__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    parser = argparse.ArgumentParser(
        prog='jobkorea crawler',
        description='jobkorea 구인목록을 크롤합니다.')
    parser.add_argument('-l', '--list')
    parser.add_argument('-o', '--overwrite', default=False)
    args = parser.parse_args()
    worknet_crawler(args.list, args.overwrite)

