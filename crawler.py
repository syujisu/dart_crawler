#필요한 모듈과 라이브러리 로딩
import requests
import json
import pandas as pd
from bs4 import BeautifulSoup
import webbrowser
from html_table_parser import parser_functions as parser
from pandas.io.json import json_normalize

from bs4 import BeautifulSoup
from selenium import webdriver
import time
import sys
import re
import math
import numpy  
import random
import os   

#사용자에게 재무제표 년도 입력받기
print("=" *80)
print("재무제표 년도 & 분기 수집")
print("=" *80)


#변수
i= 0
cnt = 0
query_txt = '유진기업_재무제표'
s_year = str(input("조회 할 년도를 입력하세요(범위 : 2016 - 2020) : "))
total_dataframe = pd.DataFrame(columns = ['접수번호', '고유번호', '종목 코드', '계정명', '개별/연결구분', '개별/연결명', '재무제표구분', '재무제표명',
       '당기명', '당기일자', '당기금액', '전기명', '전기일자', '전기금액', '계정과목 정렬순서', '당기누적금액',
       '전기누적금액'])


#사용자등록 인증키 / 회사 코드 
API_KEY="fbd3f31ee413a318c81b0fe2bc0ad8b283dcfe21"
company_code="00184667"

#분기별 url 

for i in range(11011, 11015):
    com_url = "https://opendart.fss.or.kr/api/fnlttSinglAcnt.json?crtfc_key="+API_KEY+"&corp_code="+company_code+"&bsns_year="+s_year+"&reprt_code="+str(i)
    print(com_url)
    try:
        response = requests.get(com_url)
        data = json.loads(response.content)
        df = pd.json_normalize(data['list'])
        df_dataframe = pd.DataFrame(df)
        df_dataframe.rename(columns={'rcept_no':'접수번호',
                      'corp_code':'고유번호',
                     'stock_code':'종목 코드',
                      'account_nm':'계정명',
                      'fs_div':'개별/연결구분',
                      'fs_nm':'개별/연결명',
                      'sj_div':'재무제표구분',
                      'sj_nm':'재무제표명',
                      'thstrm_nm':'당기명',
                      'thstrm_dt':'당기일자',
                      'thstrm_amount':'당기금액',
                      'frmtrm_nm':'전기명',
                      'frmtrm_dt':'전기일자',
                      'frmtrm_amount':'전기금액',
                      'bfefrmtrm_nm': '전전기명',
                      'bfefrmtrm_dt': '전전기일자',
                      'bfefrmtrm_amount': '전전기금액',
                      'ord': '계정과목 정렬순서',
                    'thstrm_add_amount' : '당기누적금액',
                    'frmtrm_add_amount' : '전기누적금액',
                     },inplace=True)
        total_dataframe = pd.concat([total_dataframe, df_dataframe])
        i += 1
        
        base_dir = "C:\py_temp"
        file_nm = s_year+ "년도_"+ query_txt +".xlsx"
        xlxs_dir = os.path.join(base_dir, file_nm)
        writer = pd.ExcelWriter(file_nm)
        total_dataframe.to_excel(writer,'Sheet1')
        writer.save()
                    
    except KeyError:
        print("error")