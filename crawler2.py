# 1. 유진기업의 총매출 이익률을 도출

#필요한 모듈과 라이브러리 로딩
from html_table_parser import parser_functions as parser
from pandas.io.json import json_normalize
from openpyxl import load_workbook
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver

import time
import sys
import re
import math
import numpy  
import random
import os  
import webbrowser
import requests
import json
import pandas as pd

#사용자등록 인증키 / 회사 코드 
API_KEY="fbd3f31ee413a318c81b0fe2bc0ad8b283dcfe21"
#유진기업
company_code="00184667"


#연결재무제표 url - 여기에 매출원가 있음
#http://dart.fss.or.kr/dsaf001/main.do?rcpNo=20170104000476&dcmNo=5403326&eleId=17&offSet=1361367&length=192053&dtd=dart3.xsd&detailYn=Y


url = "https://opendart.fss.or.kr/api/list.xml?crtfc_key="+API_KEY+"&corp_code="+company_code+"&bgn_de=20180117&end_de=20200117&page_no=1&page_count=10"
resultXML=urlopen(url)
result=resultXML.read()

xmlsoup=BeautifulSoup(result,'html.parser')


data = pd.DataFrame()
te=xmlsoup.findAll("list")

for t in te:
    temp = pd.DataFrame(([[t.corp_cls.string,t.corp_name.string,t.corp_code.string,t.stock_code.string,
                t.report_nm.string,t.rcept_no.string,t.flr_nm.string,t.rcept_dt.string,t.rm.string]]),
                columns = ["corp_cls","corp_name","corp_code","stock_code","report_nm","rcept_no","flr_nm","rcept_dt","rm"])
    data = pd.concat([data, temp])

temp
data=data.reset_index(drop=True)
url2="http://dart.fss.or.kr/dsaf001/main.do?rcpNo="+data['rcept_no'][0]
webbrowser.open(url2)


# dart api2
import time
from bs4 import BeautifulSoup
import urllib.parse as parser
import selenium
import pandas as pd
from html_table_parser import parser_functions as parser


import time
import sys
import re
import math
import numpy  
import random
import os  
import webbrowser
import requests
import json
import pandas as pd


url2="http://dart.fss.or.kr/report/viewer.do?rcpNo=20170104000476&dcmNo=5403326&eleId=17&offset=1361367&length=192053&dtd=dart3.xsd"

report=urlopen(url2)
r=report.read()

xmlsoup=BeautifulSoup(r,'html.parser')
body = xmlsoup.find("body")
table = body.find_all("table")
p = parser.make2d(table[3])


sheet = pd.DataFrame(p[2:], columns = ["구분", "33기반기_3개월", "33기_누적","32기반기_3개월", "32기_누적", "32기", "31기"])


sheet["33기반기_3개월"]=sheet["33기반기_3개월"].str.replace(",","")
sheet["temp"]=sheet["33기반기_3개월"].str[0]

sheet.loc[sheet["temp"]=="(","33기반기_3개월"]=sheet["33기반기_3개월"].str.replace("(","-")
sheet["33기반기_3개월"]=sheet["33기반기_3개월"].str.split(")").str[0]
sheet.loc[sheet["33기반기_3개월"]=="","33기반기_3개월"]="0"
sheet["33기반기_3개월"]=sheet["33기반기_3개월"].astype(float)


sale = sheet[sheet["구분"]=="수익(매출액)"].iloc[0,1]
sale_cost = sheet[sheet["구분"]=="매출원가"].iloc[0,1]
sale_profit_ratio=(sale-sale_cost)/sale*100

# round는 반올림
sale_profit_ratio=round(sale_profit_ratio,1)
print("매출총이익률은 "+str(sale_profit_ratio)+"% 입니다")


