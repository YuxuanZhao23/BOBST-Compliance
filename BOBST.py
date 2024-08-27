# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import requests
from bs4 import BeautifulSoup
import re
import csv
from time import * # 引入一个time模块， * 表示time模块的所有功能

def get_href_set(url):
    hrefSet = set()
    strhtml = requests.get(url)
    soup = BeautifulSoup(strhtml.text, 'lxml')
    # 找到所有的链接
    for a in soup.find_all('a'):
        originHref = a.get('href')
         # 链接存在，而且不是图片和pdf，带有bobst.com/且是中文zh/
        if check_href_valid(originHref):
            # 补全不完整的
            if 'http' not in originHref and 'zh/' in originHref:
                originHref = 'https://www.bobst.com' + originHref
            # 去重
            if originHref not in hrefSet:
                hrefSet.add(originHref)
    return hrefSet

def check_href_valid(href):
    formats = ['.jpg', '.pdf']
    black_list = ['/register', 'bobst.com/twitter', 'bobst.com/facebook']
    if href: # href 存在
        # 对于所有 出现了format 的链接都为 False
        for f in formats:
            if f in href:
                return False
        # 对于所有 出现了黑名单链接 的链接都为 False
        for b in black_list:
            if b in href:
                return False
        # 对于所有 不是中文 的链接都为 False，这一步会排除 '#'
        if 'cnzh/' not in href:
            return False
        # 对于所有 完整链接 来说，域名不是 bobst.com 都为 False
        elif 'http' in href and 'bobst.com/' not in href:
            return False
        else:
            return True
    else:
        return False

def check_match_valid(match, target, white_list):
    for white_word in white_list:
        if target in white_word and white_word in match:
            return False
    return True

def url_contains_string(url, input, white_list):
    try:
        strhtml = requests.get(url)
        soup = BeautifulSoup(strhtml.text, 'lxml')
        for target in input:
            reg = re.compile('.*' + target + '.*')
            matches = soup.find_all(text=reg)
            if matches != []:
                f = open('查询结果.csv', 'a')
                for match in matches:
                    if check_match_valid(match, target, white_list):
                        with f:
                            writer = csv.writer(f)
                            row = [url, target, match]
                            writer.writerow(row)
                            print(row)
        return True
    except:
        return False

def get_multi_layer_href(layer):
    if layer > 0:
        href_set = get_href_set(url)
        for i in range(layer - 1):
            for href in href_set:
                branch_href_set = get_href_set(href)
                href_set = set.union(branch_href_set, href_set)
    return href_set

def create_result_file_header():
    f = open('查询结果.csv', 'w', encoding='utf-8_sig')
    with f:
        writer = csv.writer(f)
        writer.writerow(['url', '敏感词', '内容'])

def read_non_conformity_words_from_txt():
    with open('non-conformity words.txt') as f:
        line = f.readline()
        return line.split('、')

begin_time = time() # 作用： 可以统计程序运行的时间
if __name__ == '__main__':
    url = 'https://www.bobst.com/cnzh/'
    href_set = get_multi_layer_href(2)
    print(href_set)
    create_result_file_header()
    input = read_non_conformity_words_from_txt()
    white_list = ['最终']
    print('加载敏感词和白名单完成，查询中...')
    for url in href_set:
        url_contains_string(url, input, white_list)
    end_time = time()
    run_time = end_time-begin_time
    print('加载链接{}条，运行时间：{}'.format(len(href_set), run_time))

# 引入一个time模块， * 表示time模块的所有功能，
# 作用： 可以统计程序运行的时间
#from time import *
#begin_time = time()


#end_time = time()
#run_time = end_time-begin_time
#print ('该循环程序运行时间：',run_time) #该循环程序运行时间： 1.4201874732

