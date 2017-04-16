# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import hashlib
from copy import deepcopy
from utils import mysqlClient
import datetime
import re
import logging

# init database
db = mysqlClient()
# logging
logger = logging.getLogger("dy2018_worker")  
formatter = logging.Formatter('%(name)-12s %(asctime)s %(levelname)-8s %(message)s', '%a, %d %b %Y %H:%M:%S',)  
file_handler = logging.FileHandler("/tmp/dy2018_worker.log")  
file_handler.setFormatter(formatter)
# file_handler.setLevel(logging.INFO)
# stream_handler = logging.StreamHandler(sys.stderr)  
logger.addHandler(file_handler)  
# logger.addHandler(stream_handler)  
logger.setLevel(logging.INFO)  
# logger.error("fuckgfw")  
# logger.removeHandler(stream_handler)  
# logger.error("fuckgov")  


def get_page_content(url):
    hd = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"}
    try:
        r = requests.get(url, headers=hd)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
    except:
        logger.error("open failed")
    return r.text

def find_move(html):
    soup=BeautifulSoup(html, 'html.parser')
    tbls = soup('table', attrs={"class":"tbspan"})
    movies_dict = {}
    result_lst = []
    for t in tbls:
        a = t.find('a')
        movie_name = a.text
        movies_dict['name'] = movie_name
        movies_dict['url']= "http://www.dy2018.com" + a.attrs["href"]
        movies_dict['hash'] = hashlib.md5(movie_name.encode('utf-8')).hexdigest()
        movies_dict['include_date'] = datetime.date.today()
        result_lst.append(deepcopy(movies_dict))
    logger.info('totally dag {} movies from the page'.format(len(result_lst)))
    return result_lst


def print_result(result_lst):
    tplt = "{0:{3}<40}\t{1:{3}<20}\t{2:{3}<20}"
    print(tplt.format("名字","地址", "HASH", chr(12288)))
    for i in result_lst:
        print(tplt.format(i["name"],i["url"],i["hash"],chr(12288)))

def save_movie_result(result_lst):
    counter = 1
    for i in result_lst:
        existed = db.search_movie_item(('hash', i['hash']))
        if existed: 
            logger.info('This movies already in database, skipping')
        else:
            db.add_movie_item(**i)
            counter += 1
    logger.info("saved {} movies".format(i))

def find_download_links(movie_url):
    html = get_page_content(movie_url)
    soup = BeautifulSoup(html, 'html.parser')
    a_list = soup('a')
    ftp_pattern = re.compile('ftp://.*')
    download_links = []
    for a in a_list:
        if ftp_pattern.search(a.attrs["href"]):
            download_links.append(a.text)
    logger.info("totally dag {} links for the movie".format(len(download_links)))
    return download_links

def main():
    logger.info("[+]worker start")
    url = "http://www.dy2018.com/html/gndy/dyzz/index.html"
    html = get_page_content(url)
    movie_info_list = find_move(html)
    if not movie_info_list:
        logger.warn('[!]find source are having problem!')
    save_movie_result(movie_info_list)
    for i in movie_info_list:
        movie_url = i["url"]
        dl_lst = find_download_links(movie_url)
        for dl in dl_lst:
            db.add_download_link(movie_hash=i["hash"], movie_link=dl)
    with open('/tmp/dy2018_worker_checkin', 'w') as f:
        f.write("{}".format(datetime.datetime.now()))

if __name__ == '__main__':
    main()