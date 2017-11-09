import requests
from bs4 import BeautifulSoup
import traceback
import os


def get_HTML_text(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) \
                                  AppleWebKit/537.36 (KHTML, like Gecko) \
                                  Chrome/48.0.2564.82 Safari/537.36'}
        r = requests.get(url, headers=headers, timeout=30)
        r.raise_for_status
        if r.status_code !== '200':
     		print('%s，爬虫中断!' % (r.status_code))
        	exit()
        r.encoding = 'utf-8'
        return r.text
    except Exception as ex:
        return ''


def get_parsed_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    img_urls = []
    for img in soup.find_all('a', text='[查看原图]'):
        img_urls.append('http:' + img.get('href'))
    next_url = 'http:' + soup.find(title='Older Comments').get('href')
    return (img_urls, next_url)


def download_and_save_imgs_to_file(img_urls, save_path):
    for img_url in img_urls:
        try:
            img_name = img_url.split('/')[-1]
            r = requests.get(img_url)
            r.raise_for_status
            print(save_path + img_name)
            with open(save_path + img_name, 'wb') as f:
                f.write(r.content)
        except Exception as ex:
            continue


def main():
    url = 'http://jandan.net/ooxx'
    depth = 500
    dir_path = 'E://xxoo/'
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    for i in range(depth):
        print('正在爬取第%d页...' % (i + 1))
        try:
            html = get_HTML_text(url)
            img_urls, url = get_parsed_data(html)
            download_and_save_imgs_to_file(img_urls, dir_path)
        except Exception as ex:
            continue


main()
