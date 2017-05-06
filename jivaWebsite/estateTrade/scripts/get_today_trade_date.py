#coding=utf-8
import requests
from bs4 import BeautifulSoup
from copy import deepcopy
import utils
import json
import time
import random
import datetime
import sys

DB = utils.mysqlClient()

def get_page_content(url):
    hd = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"}
    try:
        r = requests.get(url, headers=hd)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
    except:
        print("open failed")
    return r.text

def get_validated_tradedata_day_list():
    last_checked_date = DB.get_last_trade_date()[0]
    url = 'http://www.nnfcj.gov.cn/tradedataDayList_1.jspx'
    tradedata_day_list = []
    html = get_page_content(url)
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table')
    tr_lst = table.find_all('tr')
    for tr in tr_lst[1:]: # first tr tag is table head
        td_lst = tr.find_all('td')
        tradedata_day = td_lst[0].text
        tradedata_day_year = int(tradedata_day.split('-')[0])
        tradedata_day_month = int(tradedata_day.split('-')[1])
        tradedata_day_day = int(tradedata_day.split('-')[2])
        today= datetime.date.today()
        tradedata_day_obj = today.replace(year=tradedata_day_year,
            month=tradedata_day_month,
            day=tradedata_day_day)
        if tradedata_day_obj > last_checked_date:
            print('got validated date: {}'.format(tradedata_day))
            tradedata_day_list.append(tradedata_day)
    return tradedata_day_list


def get_trade_detail_by_usage(trade_date):
    """
    按用途
    :param trade_date:
    :return:
    """
    detail_url = 'http://www.nnfcj.gov.cn/tradedataDayDetail.jspx?houseCtgId=0&ctgId=0&dateString={}'.format(trade_date)
    detail_html = get_page_content(detail_url)
    detail_soup = BeautifulSoup(detail_html, 'html.parser')
    detail_table = detail_soup.find('table')
    detail_tr_lst = detail_table.find_all('tr')
    trade_date_detail_lst = []
    for tr in detail_tr_lst[2:-1]:
        trade_date_detail = {}
        td_lst = tr.find_all('td')
        trade_date_detail['district'] = td_lst[0].text.strip()
        trade_date_detail['apartment_amount'] = td_lst[1].text.strip()
        trade_date_detail['acreage_amount'] = td_lst[2].text.strip()
        trade_date_detail['trade_date'] = trade_date
        trade_date_detail_lst.append((deepcopy(trade_date_detail)))
    return trade_date_detail_lst

def wirte_into_db(trade_date_list):
    
    for trade in trade_date_list:
        DB.add_item(**trade)
        print('saved {}'.format(trade))


def main():
    # validated sources date is not already been store at database
    tradedata_day_list = get_validated_tradedata_day_list()
    if tradedata_day_list:
        print("got date list")
    else:
        print("not date got, exit")
        sys.exit()
    # set a result contain
    result = []
    for trade_date in tradedata_day_list:
        print('handling {}'.format(trade_date))
        result.append(get_trade_detail_by_usage(trade_date)) # requests data from sources 
    for i in result:
        wirte_into_db(i) # save results
    # write running time for checking
    with open('/tmp/get_estate_trade_worker_checkin', 'w') as f:
        f.write("{}".format(datetime.datetime.now()))
if __name__ == '__main__':
    main()