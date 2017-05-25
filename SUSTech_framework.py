__author__ = 'Boris'

import requests
import re
from bs4 import BeautifulSoup
import html
from lxml.html.soupparser import unescape
import json

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
        self.url = 'https://cas.sustc.edu.cn/cas/login?service='+site
        self.s = requests.session()
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

class ClassInfo():
    def __init__(self, databox):
        self.teacher = databox['skls']
        self.course_name = databox['kcmc']
        self.course_id = databox['kch']
        self.course_major = databox['dwmc']
        self.course_selector = databox['jx0404id']
        
    def __str__(self):
        s = '课程名：{} 课程号：{} 授课教师：{} 所属院系：{} '.format(self.course_name, self.course_id, self.teacher, self.course_major)
        s = s.replace('None', 'Unknown')
        s = html.unescape(s)
        return s

    def contains(self, text):
        info = str(self)
        return text in info


def search(course_list, text):
    return_list = []
    text = text.upper()
    for course in course_list:
        if course.contains(text):
            return_list.append(course)
    return return_list

def get_url_courses(sustc, url):
    post_data = {
        'sEcho': 1,
        'iColumns':1,
        'sColumns': None ,
        'iDisplayStart':0,
        'iDisplayLength':100,
        'mDataProp_0':'kch', # 课程号
        # 'mDataProp_1':'kcmc', # 课程名
        # 'mDataProp_2':'xf', # 学分
        # 'mDataProp_3':'skls', # 上课老师
        # 'mDataProp_4':'sksj', # 上课时间
        # 'mDataProp_5':'skdd', # 上课地点
        # 'mDataProp_6':'xkrs', # 
        # 'mDataProp_7':'syrs', # 剩余量
        # 'mDataProp_8':'ctsm', # 时间冲突
        # 'mDataProp_9':'czOper', # 操作
    }
    data = json.loads(sustc.post_website(url, post_data))
    cross_major_course_list = []
    for dict_ in data['aaData']:
        cross_major_course_list.append(ClassInfo(dict_))
    return cross_major_course_list

def try_to_select(sustc, course_selector):
    jx0404id = course_selector
    xkzy = ''
    trjf = ''
    post_data = {
        'jx0404id': jx0404id,
        'xkzy':xkzy,
        'trjf':trjf,
    }

    return (sustc.get_website('http://jwxt.sustc.edu.cn/jsxsd/xsxkkc/fawxkOper', post_data))

def get_selected_course(sustc):
    text = sustc.get('http://jwxt.sustc.edu.cn/jsxsd/xsxkjg/comeXkjglb')
    soup = BeautifulSoup(text, 'lxml')
    tbody = soup.find('tbody')
    trs = tbody.find_all('tr')
    selected_courses = []
    for tr in trs:
        tds = tr.find_all('td')
        formula = '\d+'
        pattern = re.compile(formula)
        jx0404id = (re.search(pattern, tds[-1].a['href']).group())
        dict_ = {
            'skls': tds[4].text,
            'kcmc': tds[1].text,
            'kch': tds[0].text,
            'dwmc': '',
            'jx0404id': jx0404id,
        }
        course = ClassInfo(dict_)
        print(course)
        selected_courses.append(course)
    return selected_courses

def get_all_courses(sustc):
    #专业内选课
    in_major_courses = get_url_courses(sustc, 'http://jwxt.sustc.edu.cn/jsxsd/xsxkkc/xsxkKnjxk?kcxx=&skls=&skxq=&skjc=&sfym=false&sfct=false')

    #跨专业选课
    cross_major_courses = get_url_courses(sustc, 'http://jwxt.sustc.edu.cn/jsxsd/xsxkkc/xsxkFawxk?kcxx=&skls=&skxq=&skjc=&sfym=false&sfct=false')

    #本学期选课计划
    this_term_courses = get_url_courses(sustc, 'http://jwxt.sustc.edu.cn/jsxsd/xsxkkc/xsxkBxqjhxk?kcxx=&skls=&skxq=&skjc=&sfym=false&sfct=false')

    #公选课计划
    public_courses = get_url_courses(sustc, 'http://jwxt.sustc.edu.cn/jsxsd/xsxkkc/xsxkGgxxkxk?kcxx=&skls=&skxq=&skjc=&sfym=false&sfct=false&szjylb=')
    return {'in_major_courses': in_major_courses, 
            'cross_major_courses': cross_major_courses,
            'this_term_courses': this_term_courses,
            'public_courses': public_courses }

class MyApp(QtGui.QMainWindow, Ui_MainWindow):
    """docstring for MyApp"""
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        
