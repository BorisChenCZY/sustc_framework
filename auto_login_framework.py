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

class SUSTech(object):

    """
    docstring for Sakai,
    this code is to get Sakai page for SUSTC students, they can get necessary
    information such as course slices or assignments from this modual
    """

    def __init__(self, username, password, site):

        """
        to init Sakai, username and password is in need
        """
        self.site = site
        self.headers = {
            "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3)' +
                          ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/' +
                          '56.0.2924.87 Safari/537.36'}
        self.data = {
            'username': str(username),
            'password': str(password),
            #     'lt': lt,
            #     'excusion': execution,
            '_eventId': 'submit',
            'submit': 'LOGIN',
        }
        self.s = requests.session()
        r = self.s.get(site)
        self.url = r.url
        # print(r.url)
        # print(r.text)
        # self.url = 'https://cas.sustc.edu.cn/cas/login?service='+site
        # print(self.url)
        r = self.s.get(self.url, headers = self.headers)
        content = r.content.decode('utf-8')
        self.data['execution'] = self._get_execution(content)
        self.data['lt'] = self._get_lt(content)
        self.loggedIn = False
        self.topped_sites = {}
        self.other_sites = {}
        self.sites = {}

    def _get_execution(self, content):
        formula = '<input.*?name="execution".*?value="(.*?)" />'
        pattern = re.compile(formula)
        return re.findall(pattern, content)[0]

    def _get_lt(self, content):
        formula = '<input.*?name="lt".*?value="(.*?)" />'
        pattern = re.compile(formula)
        return re.findall(pattern, content)[0]

    def login(self):
        self.s.post(self.url, self.data)
        text = self._get_home_page()
        self.loggedIn =  'CAS' not in text
        return self.loggedIn

    def _check_logged(self):
        if not self.loggedIn:
            print('not logged in, permission denied')
        return self.loggedIn

    def _get_home_page(self):
        r = self.s.get(self.site)
        text = r.content.decode('utf-8')
        txt = unescape(text)
        return txt

    def get_home_page(self):
        if not self._check_logged():
            return
        return self._get_home_page()

    def get_home_soup(self):
        if not self.loggedIn:
            raise Exception('not logged in yet!')
        r = self.s.get(self.site)
        soup = BeautifulSoup(r.text, 'lxml')
        return soup

    def get_cookies(self):
        return self.s.cookies

    def get_website(self, url, paras = None):
        if not self.loggedIn:
            return 
        r = self.s.get(url, params = paras)
        # print(r.url)
        return r.text

    def post_website(self, url, post_data):
        r = self.s.post(url, data = post_data)
        return r.text

    def get(self, *args):
        return self.get_website(*args)

    def post(self, *args):
        return self.post_website(*args)

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
