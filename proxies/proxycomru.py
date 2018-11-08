# -*- coding: utf-8 -*-

from getproxies import *
import requests
import re
import httplib
import HTMLParser
import lxml.html
from lxml.cssselect import CSSSelector
from lxml import etree

class proxydotcomscraper(proxyscraper):
    def __init__(self):
        proxyscraper.__init__(self)
        self.baseurl = "http://www.proxy.com.ru"
        self.proxy_website = "proxy.com.ru"
    def build_proxy_page_urls(self):
        conn = httplib.HTTPConnection("www.proxy.com.ru")
        r = conn.request("GET","/")
        response = conn.getresponse().read()
        conn.close()   
        #print response.decode('gbk').encode('utf-8')
        reg_exp = re.compile(".*共([0-9]+)页.*")
        for line in response.split("\n"):
            result = reg_exp.match(line.decode('gbk').encode('utf-8'))
            if result <> None:
                page = int(result.group(1))
                break

        self.proxy_page_urls = ["%s/list_%d.html"%(self.baseurl,p) for p in range(1,page+1) ]

    def _parse_response(self, response):
        #xpath: /html/body/center/font/table[1]/tbody/tr/td[2]/font/table
        #csspath: body > center > font > table:nth-child(1) > tbody > tr > td:nth-child(2) > font > table        
        response = proxydotcomscraper._html_unescape(response.decode('gbk').encode('utf-8'))

        proxies = []
        proxy_pattern = re.compile('<tr><b><td>[0-9]+</td><td>([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)</td><td>([0-9]+)</td>')
        for line in response.split('\n'):

            result = proxy_pattern.match(line)
            if result == None:
                continue
            if len(result.groups()) >= 2:
                p = theproxy()                
                p.ip =  result.group(1).strip()
                p.port = int(result.group(2).strip())
                proxies.append(p)                       
        return proxies

    @staticmethod
    def _html_unescape(html):
        html = html.replace("&lt;","<")
        html = html.replace("&gt;",">")
        return html

if __name__ == "__main__":
    ps = proxydotcomscraper()
#    ps.build_proxy_page_urls()
#    for p in ps.proxy_page_urls:
#        print p
    #ps._parse_response(open("view-source www.proxy.com.ru.html").read())
   #proxydotcomscraper._html_unescape("&lt;b&gt;")
    ps.scrape_proxies()
