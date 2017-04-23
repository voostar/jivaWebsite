#!coding=utf-8

import requests
from bs4 import BeautifulSoup
from copy import deepcopy
import utils
import json
import time
import random

def get_page_content(url):
    hd = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"}
    try:
        r = requests.get(url, headers=hd)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
    except:
        print("open failed")
    return r.text

def get_tradedata_day_list():
    url_tmp = 'http://www.nnfcj.gov.cn/tradedataDayList_{}.jspx'
    tradedata_day_list = []
    for i in range(1, 226):
        url = url_tmp.format(i)
        html = get_page_content(url)
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('table')
        tr_lst = table.find_all('tr')
        for tr in tr_lst[1:]: # first tr tag is table head
            td_lst = tr.find_all('td')
            tradedata_day = td_lst[0].text
            print('got date: {}'.format(tradedata_day))
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
    db = utils.mysqlClient()
    for trade in trade_date_list:
        db.add_item(**trade)
        print('saved {}'.format(trade))

def compare_last_check():
    url_tmp = 'http://www.nnfcj.gov.cn/tradedataDayList_1.jspx'
    html = get_page_content(url)
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table')
    tr = table.find_all('tr')[1]
    last_trade_date = tr.find_all('td')[0].text
    with open('last_check.json', 'r') as f:
        last_check_json = json.loads(f.read())
    if last_trade_date == last_check_json['checked_date']:
        print('no new trade date found')
        return False
    else:
        return True

def send_ftqq_msg(ftqq_msg):
    r = requests.get('http://sc.ftqq.com/SCU7414T2747b9eccc4e897e12cdd8c68314c14b58ec773fab33c.send?text={}'.format(ftqq_msg))

def main():
    start_time = time.time()
    tradedata_day_list = get_tradedata_day_list()
    print("got date list")
    result = []
    counter = 1
    for trade_date in tradedata_day_list:
        print('handling {}'.format(trade_date))
        result.append(get_trade_detail_by_usage(trade_date))
        if counter==10:
            sleep_time = random.randrange(100)
            print("going to sleep {}s".format(sleep_time))
            time.sleep(sleep_time)
            counter = 1
        counter +=1
    for i in result:
        wirte_into_db(i)
    end_time = time.time()
    send_ftqq_msg("主人，任务完成，耗时{}分钟。".format((end_time - start_time)/60))

if __name__ == '__main__':
    main()