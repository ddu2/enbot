#!/usr/bin/env python
#coding:utf-8
# date: 2016-03-29 
# author: dudp@foxmail.com

import re
import urllib
import urllib2
import cookielib
import mechanize
from bs4 import BeautifulSoup

login_url = 'https://login.salesforce.com'
home_page = 'https://na7.salesforce.com'
cookie_file = './.cookie'

username = 'xxxxxxxxxx'
password = 'xxxxxxxx'

def get_post_data(content,email):
    html_proc = BeautifulSoup(content,'lxml')
    _confirmationtoken = html_proc.find("input",id='_CONFIRMATIONTOKEN').get('value')
    cancelURL = html_proc.find("input",id='cancelURL').get('value')
    retURL = html_proc.find("input",id='retURL').get('value')
    save_new_url = html_proc.find("input",id='save_new_url').get('value')
    vcsrf = html_proc.find("input",id='vcsrf').get('value')
    vpol = html_proc.find("input",id='vpol').get('value')
    vflid = html_proc.find("input",id='vflid').get('value')
    vfgrp = html_proc.find("input",id='vfgrp').get('value')
    code = raw_input("Please input your verification code: ")
    save = 'Verify'
    postdata = { 
        '_CONFIRMATIONTOKEN':_confirmationtoken,
        'cancelURL':cancelURL,
        'retURL':retURL,
        'save_new_url':save_new_url,
        'vcsrf':vcsrf,
        'vpol':vpol,
        'retURL':retURL,
        'vflid':vflid,
        'vfgrp':vfgrp,
        'smc':code,
        'save':save
    }
    if email:
        postdata.pop('smc')
        postdata['emc'] = code
    print urllib.urlencode(postdata)
    return urllib.urlencode(postdata)

def request(url,data=None):
    response = browser.open(url,data)
    browser._ua_handlers['_cookies'].cookiejar.save(cookie_file, ignore_discard=True, ignore_expires=True)
    return response


acc_pwd = { 'un': username, 'pw': password}

cookiejar = cookielib.LWPCookieJar()
try:
    cookiejar.load(cookie_file, ignore_discard=True, ignore_expires=True)
except IOError:
    pass

browser = mechanize.UserAgent()
browser.set_handle_robots(False)
browser.set_cookiejar(cookiejar)
browser.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0')]
browser.addheaders.append(('Referer', home_page))

try:
    data = urllib.urlencode(acc_pwd)
    response = request(login_url,data)
    content = response.read().decode('utf-8')
    status = response.code
    if status == 200:
        patern = u'Verify Your Identity'
        if re.search(patern,content):
            new_url = response.geturl()
            email = re.search('EmailVerification',new_url)
            data2 = get_post_data(content,email)
            response = request(new_url,data2)
        print response.geturl()
except urllib2.HTTPError as e:
    print "Failed to open ", home_page, str(e)
