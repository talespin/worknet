#!/usr/bin/python
"""
:filename: worknet_list.py
:author: 최종환
:last update: 2024.01.20
 
:CHANGELOG:
    ============== ========== ====================================
    수정일            수정자        수정내용
    ============== ========== ====================================
    2024.01.20     최종환        최초생성
    ============== ========== ====================================
 
:desc:
    워크넷 site 의 전체 지역 체용정보 목록조회 생성
 
"""
import os
import sys
import math
import logging
import pandas as pd
import requests as req
from time import sleep
from datetime import datetime
from bs4 import BeautifulSoup as bs


logging.basicConfig(level=logging.INFO, stream=sys.stdout)

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

params = {
    'careerTo': '',
    'keywordJobCd': '',
    'occupation': '',
    'templateInfo': '',
    'shsyWorkSecd': '',
    'rot2WorkYn': '',
    'payGbn': '',
    'resultCnt': '1000',
    'keywordJobCont': '',
    'cert': '',
    'cloDateStdt': '',
    'moreCon': '',
    'minPay': '',
    'codeDepth2Info': '11000',
    'isChkLocCall': '',
    'sortFieldInfo': 'DATE',
    'major': '',
    'resrDutyExcYn': '',
    'eodwYn': '',
    'sortField': 'DATE',
    'staArea': '',
    'sortOrderBy': 'DESC',
    'keyword': '',
    'termSearchGbn': 'all',
    'carrEssYns': '',
    'benefitSrchAndOr': 'O',
    'disableEmpHopeGbn': '',
    'webIsOut': 'region',
    'actServExcYn': '',
    'maxPay': '',
    'keywordStaAreaNm': '',
    'emailApplyYn': '',
    'listCookieInfo': 'DTL',
    'pageCode': '',
    'codeDepth1Info': '11000',
    'keywordEtcYn': '',
    'publDutyExcYn': '',
    'keywordJobCdSeqNo': '',
    'exJobsCd': '',
    'templateDepthNmInfo': '',
    'computerPreferential': '',
    'regDateStdt': '',
    'employGbn': '',
    'empTpGbcd': '',
    'region': '',
    'infaYn': '',
    'resultCntInfo': '1000',
    'siteClcd': 'all',
    'cloDateEndt': '',
    'sortOrderByInfo': 'DESC',
    'currntPageNo': '1',
    'indArea': '',
    'careerTypes': '',
    'searchOn': 'Y',
    'tlmgYn': '',
    'subEmpHopeYn': '',
    'academicGbn': '',
    'templateDepthNoInfo': '',
    'foriegn': '',
    'mealOfferClcd': '',
    'station': '',
    'moerButtonYn': '',
    'holidayGbn': '',
    'srcKeyword': '',
    'enterPriseGbn': 'all',
    'academicGbnoEdu': 'noEdu',
    'cloTermSearchGbn': 'all',
    'keywordWantedTitle': '',
    'stationNm': '',
    'benefitGbn': '',
    'keywordFlag': '',
    'notSrcKeyword': '',
    'essCertChk': '',
    'isEmptyHeader': '',
    'depth2SelCode': '',
    '_csrf': '847af1b2-e7bf-4b52-a903-e69695122a91',
    'keywordBusiNm': '',
    'preferentialGbn': '',
    'rot3WorkYn': '',
    'pfMatterPreferential': '',
    'regDateEndt': '',
    'staAreaLineInfo1': '11000',
    'staAreaLineInfo2': '1',
    'pageIndex': '1',
    'termContractMmcnt': '',
    'careerFrom': '',
    'laborHrShortYn': '',
}
pageIndex = 1
total_page = 10
result = []
while True:
    logging.info(f'pageIndex={pageIndex} / {total_page}')
    if os.path.exists(f'../list/{pageIndex}'):
        with open(f'../list/{pageIndex}','rb') as fs:
            doc = bs(fs.read(), 'html.parser')
    else:
        sleep(5)
        res = req.get(f'{base_url}/empInfo/empInfoSrch/list/dtlEmpSrchList.do', params=params, cookies=cookies, headers=headers)
        with open(f'../list/{pageIndex}','wb') as fs:
            fs.write(res.content)
        doc = bs(res.content, 'html.parser')
    items = doc.find('table', {'class':'board-list'}).find('tbody').find_all('tr')
    for item in items:
        회사명, 채용공고처, 채용공고명, 지원자격, 지역, 근무조건, 등록_마감일 = '', '', '', '', '', '', ''
        tds = item.find_all('td')
        try:
            id = [x for x in tds[2].find('a').get('href').split('?')[1].split('&') if x.startswith('wantedAuthNo=')][0].split('=')[1]
        except:
            try:
                id = [x for x in tds[2].find('a').get('href').split('?')[1].split('&') if x.startswith('easyWantedRegNo=')][0].split('=')[1]
            except:
                try:
                    id = [x for x in tds[2].find('a').get('href').split('?')[1].split('&') if x.startswith('empSeq=')][0].split('=')[1]
                except:
                    id = tds[2].find('a').get('onclick').split("'")[1]
        url = base_url + tds[2].find('a').get('href')
        try:
            회사명 = tds[1].find('a').text.strip()
        except:
            회사명 = tds[1].text.strip().split('\n')[0]
        채용공고처 = tds[1].find_all('div')[-1].text.strip()
        채용공고명 = tds[2].find('div', {'class':'cp-info-in'}).text.strip()
        try:
            담당업무 = item.find('script').text.split('\n')[4].strip().split("'")[-2].strip()
        except:
            pass
        line3 = [x.text.strip()  for x in tds[2].find_all('em')]
        try:
            지원자격 = ','.join(line3[:-1])
        except:
            pass
        try:
            지역 = line3[-2]
        except:
            pass
        try:
            근무조건 = ','.join([x for x in tds[3].text.split('\n') if x !=''])
        except:
            pass
        try:
            등록_마감일 = '\n'.join([x.strip() for x in tds[4].text.split('\n') if x!=''])
        except:
            pass
        result.append(dict(id=id, url=url, 회사명=회사명, 채용공고처=채용공고처, 채용공고명=채용공고명, 담당업무=담당업무, 지원자격=지원자격, 지역=지역, 근무조건=근무조건, 등록_마감일=등록_마감일))
    total_cnt = int(doc.find_all('strong', {'class':'font-orange'})[-1].text.replace(',',''))
    total_page = math.ceil(total_cnt / 1000)
    pageIndex += 1
    params.update({'pageIndex':pageIndex})
    if pageIndex > total_page: break
os.makedirs('../list', exist_ok=True)
pd.DataFrame(result).to_excel('../list/worknet_list.xlsx', index=False)    
logging.info('worknet crawl list end:' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

#if __name__=='__main__':
#logging.baseConfig(level=logging.info, stream=sys.stdout)
#    main()