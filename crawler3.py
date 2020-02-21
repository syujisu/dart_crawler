# 2.유진기업, 유진투자증권, 동양에 대하여 일괄로 작업하도록 작성해 보십시오

from urllib.request import urlopen
import pandas as pd
from bs4 import BeautifulSoup
import webbrowser
from html_table_parser import parser_functions as parser

API_KEY="fbd3f31ee413a318c81b0fe2bc0ad8b283dcfe21"

#함수 내 사용할 변수 선언

def make_report(company_code):
    url = "http://dart.fss.or.kr/api/search.xml?auth="+API_KEY+"&crp_cd="+company_code+"&start_dt=19990101&bsn_tp=A001&bsn_tp=A002&bsn_tp=A003"
    resultXML=urlopen(url)
    result=resultXML.read()
    xmlsoup=BeautifulSoup(result,'html.parser')
    data = pd.DataFrame()
    te=xmlsoup.findAll("list")

    for t in te:
        temp=pd.DataFrame(([[t.crp_cls.string,t.crp_nm.string,t.crp_cd.string,t.rpt_nm.string,
                        t.rcept_no.string,t.flr_nm.string,t.rcept_dt.string, t.rmk.string]]),
                          columns=["crp_cls","crp_nm","crp_cd","rpt_nm","rcept_no","flr_nm","rcept_dt","rmk"])
        data=pd.concat([data,temp])
    
    
    data=data.reset_index(drop=True)
    url2="http://dart.fss.or.kr/dsaf001/main.do?rcept_no="+data['rcept_no'][0]
    return url2, data['rcept_no'][0]


def find_table(url2,rcept_no):
    temp=urlopen(url2)
    r=temp.read()
    xmlsoup=BeautifulSoup(r,'html.parser')
    temp=xmlsoup.find_all("script",attrs={"type":"text/javascript"})
    txt=temp[7]
    a=txt.text

    b=str.find(a,"4. 재무제표")
    c=a[b:b+200]
    d=c.split(",")[4]
    e=d.replace("\"","")
    e=e.replace("\'","")
    dcmo=int(e)


    url3="http://dart.fss.or.kr/report/viewer.do?rcept_no="+rcept_no+"&dcmNo="+str(dcmo)+"&eleId=15&offset=297450&length=378975&dtd=dart3.xsd" 
    
    report=urlopen(url3)
    r=report.read()
    xmlsoup=BeautifulSoup(r,'html.parser')
    body=xmlsoup.find("body")
    table=body.find_all("table")
    p = parser.make2d(table[3])


    name_list=list()
    value_list=list()

    name_list.append("구분")

    for i in range(1,len(p[0])):
        name=p[0][i]+"_"+p[1][i]
        name=name.replace(" ","")
        name_list.append(name)
        value_list.append(name)


    sheet = pd.DataFrame(p[2:], columns=name_list)
    sheet.ix[sheet["구분"]=="수익(매출액)",["구분"]]="매출액"

    return sheet, name_list, value_list



def make_profit(sheet,name_list,value_list):
    for time in value_list:
        sheet[time]=sheet[time].str.replace(",","")
        sheet["temp"]=sheet[time].str[0]
        sheet.loc[sheet["temp"]=="(",time]=sheet[time].str.replace("(","-")
        sheet[time]=sheet[time].str.split(")").str[0]
        sheet.loc[sheet[time]=="",time]="0"
        sheet[time]=sheet[time].astype(int)



    temp_list=list()
    temp_list.append("매출총이익률")



    for time in range(len(value_list)):
        sale = sheet[sheet["구분"]=="매출액"].iloc[0,time+1]
        sale_cost = sheet[sheet["구분"]=="매출원가"].iloc[0,time+1]
        sale_profit_ratio=(sale-sale_cost)/sale*100
        sale_profit_ratio = round(sale_profit_ratio, 1)
        temp_list.append(sale_profit_ratio)

    output=pd.DataFrame([temp_list],columns=name_list)


    return output
   

company_list=list(["023410","001200","001520"])

company_name=list(["유진기업","유진증권","동양"])



output_last=pd.DataFrame(columns=["구분", "최근_분기", "최근_분기_누적","이전_분기","이전_분기_누적"])





for i in range(len(company_list)):
    try:
        url2, rcept_no=make_report(company_list[i])
        sheet, name_list, value_list = find_table(url2, rcept_no)
        output = make_profit(sheet, name_list, value_list)

        if len(output.columns)==3:
            output.columns = ["구분", "최근_분기", "최근_분기_누적"]

        elif len(output.columns)==5:
            output.columns = ["구분", "최근_분기", "최근_분기_누적","이전_분기","이전_분기_누적"]

        output["company_code"]=company_list[i]
        output["company_name"] = company_name[i]
        output["url"] = url2
        output_last=pd.concat([output_last,output])

    except Exception as e:
        print(company_name[i]+" is error")
        print(e)

    output_last.to_csv("output_last.csv")