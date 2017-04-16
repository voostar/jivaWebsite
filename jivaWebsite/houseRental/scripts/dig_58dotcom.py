# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import hashlib
from copy import deepcopy
from utils import mysqlClient
import datetime
import time
import re
import sys
import logging

# init database
db = mysqlClient()
# logging
logger = logging.getLogger("58dotcom_worker")  
formatter = logging.Formatter('%(name)-12s %(asctime)s %(levelname)-8s %(message)s', '%a, %d %b %Y %H:%M:%S',)  
file_handler = logging.FileHandler("/tmp/58dotcom_worker.log")  
file_handler.setFormatter(formatter)
logger.addHandler(file_handler) 
logger.setLevel(logging.INFO)   

URL_TEMPLATE = 'http://nn.58.com/{district}/zufang/pn{index}'
DISTRICT_LIST = ['qingxiu', 'xingning', 'jiangnan', 'xixiangtang', 'yongning', 'liangqing',]

def get_page_content(url):
	print("requesting {}".format(url))
	hd = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"}
	try:
		r = requests.get(url, headers = hd, timeout = 30)
		print("requests done")
		r.raise_for_status()
		r.encoding = r.apparent_encoding
	except:
		logger.error("open {} failed".format(url))
		return False
	else:
		return r.text

def get_house_info(html, district):
	"""
	find out information and put into a dict
	"""
	soup=BeautifulSoup(html, 'html.parser')
	print("soup done")
	li_lst = soup('li' , attrs={"logr":re.compile('.*@.*')})
	result_lst = []
	for house in li_lst:
		house_info = {}
		house_info['url'] = house.find('a').attrs['href']
		house_info['name'] = house.find('h2').text.strip()
		house_info['district'] = district
		# 58.com not show all house information in list page, so here it need to dig every house links for detail
		house_detail = get_page_content(house_info['url'])
		if not house_detail:
			continue
		house_soup=BeautifulSoup(house_detail, 'html.parser')
		try:
			house_info['price'] = house_soup.find('div', attrs={'class':re.compile('^house-pay-way.*')}).b.text
		except:
			send_ftqq_msg("被屏蔽了！")
			sys.exit()
		ul_list = house_soup.find('ul', attrs={'class':"f14"}).find_all('li')
		try:
			house_info['house_type'] = ul_list[1].text.split()[0].split('：')[1]
		except:
			house_info['house_type'] = '未标注'
		try:
			house_info['acreage'] = ul_list[1].text.split()[1]
		except:
			house_info['acreage'] = '未标注'
		try:
			house_info['estate'] = ul_list[3].text.split()[0].split('：')[1]
		except:
			house_info['estate'] = '未标注'
		try:
			house_info['street'] = ul_list[4].text.split()[2]
		except:
			house_info['street'] = '未标注'
		house_info['source'] = '58.com'
		house_info['include_date'] = datetime.date.today()
		result_lst.append(deepcopy(house_info))
	return result_lst


def save_entry(info_dict):
	"""
	save a house info into data base
	"""
	exist_check = db.search_item(('url', info_dict['url']))
	if not exist_check:
		print("{} good to save".format(info_dict['url']))
		db.add_item(**info_dict)
		print("{} saved".format(info_dict['url']))
	else:
		print("{} already exists".format(info_dict['url']))

def handle_entries(html, district):
	"""
	get and save
	"""
	page_results = get_house_info(html, district)
	save_counter = 1
	for i in page_results:
		save_entry(i)
		save_counter+=1
	print('total saved {} entries'.format(save_counter))


def generate_district_url(district):
	"""
	generate 100 url for each district
	"""
	for i in range(1, 20):
		url = URL_TEMPLATE.format(
			district = district,
			index = i)
		yield url

def send_ftqq_msg(ftqq_msg):
	r = requests.get('http://sc.ftqq.com/SCU7414T2747b9eccc4e897e12cdd8c68314c14b58ec773fab33c.send?text={}'.format(ftqq_msg))

def cradlesong(sleep_duration):
	"""
	sleep
	"""
	for s in range(sleep_duration, 0, -1):
		time.sleep(1)
		print("\r{}s to continue...".format(s),end="")
	print("Awaked, start next steps")

def main():
	worker_start_time = time.time()
	for d in DISTRICT_LIST:
		send_ftqq_msg("主人，开始处理{}的信息".format(d))
		start_time = time.time()
		for url in generate_district_url(d):
			html = get_page_content(url)
			if not html:
				continue
			handle_entries(html,d)
			print("Going to sleep 10mins for avoid blocked house list")
			cradlesong(600)
		end_time = time.time()
		cost_time = end_time - start_time
		print("Round cost: {}s".format(cost_time))
		send_ftqq_msg("主人，已经处理完{}的信息了!耗时{}分钟。".format(d, int(cost_time / 60)))
		print("Going to sleep 4hours for avoid blocked house list")
		cradlesong(14400)
	worker_end_time = time.time()
	worker_cost_time = worker_end_time - worker_start_time
	print("Worker cost: {}s".format(worker_cost_time))
	send_ftqq_msg("主人，worker已完成工作，耗时{}分钟。".format(int(worker_cost_time / 60)))

if __name__ == '__main__':
	main()
