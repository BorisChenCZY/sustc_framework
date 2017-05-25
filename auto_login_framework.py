import requests
import re
from bs4 import BeautifulSoup
import html
from lxml.html.soupparser import unescape
import json
import pickle
from selenium import webdriver
import selenium
import sys
from SUSTech_framework import *

if __name__ == '__main__':
    url = requests.get('http://baidu.com').url
    if '10000' not in url:
        print('You have already logged in')
        quit()
    url = url.replace('transfer', 'index')
    students_number = 23333
    password = 32222
    sustc = SUSTech(student_number, password, url)
    sustc.login()
    # print(sustc.s.get(url))
    r = sustc.s.get('http://www.baidu.com')
    print(r.content)
