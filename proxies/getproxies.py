#!/usr/bin/python
import lxml.html
from lxml.cssselect import CSSSelector

import httplib
import string
import simplejson
import re
import requests
from urlparse import urlparse

import multiprocessing



def _test_proxy(proxy):
    ok = False
    try:
        r = requests.get('http://www.baidu.com/',timeout=5, proxies = {"http": '%s:%d'%(proxy.ip,proxy.port)})
        if r.status_code == 200:
            ok = True
    except Exception,e:
        pass
    print "%s:%s:%d, %s"%(proxy.protocol, proxy.ip, proxy.port, ok),

    return ok


def _test_proxies(proxies):
    return [ {"ip":p.ip,"port":p.port,"protocol":p.protocol} for p in proxies if _test_proxy(p)]


class theproxy:
    def __init__(self):
        self.ip = ""
        self.port = 0
        self.protocol = ""
        self.country = ""
        self.speed = 0
    def __str__(self):
        return "ip:%s\nport:%d\nprotocol:%s\ncountry:%s\nspeed:%d\n"%(self.ip,self.port,self.protocol,self.country,self.speed)

class proxyscraper:
    def __init__(self):
        self.proxy_page_urls = []
        self.proxy_website = "default"

    def build_proxy_page_urls(self):
        #overwritable
        pass

    def _scrape_single_page_proxies(self, proxy_page_url):
        try:
            url_components = urlparse(proxy_page_url)
            conn = httplib.HTTPConnection(url_components.netloc)
            r = conn.request("GET",url_components.path)
            response = conn.getresponse().read()
            conn.close() 
        except Exception:
            return []
        return self._parse_response(response)

    def _parse_response(self, response):
        return [] 

    def scrape_proxies(self):
        proxies = []
        valid_proxies = []
        self.build_proxy_page_urls()
        
        pages_num = len(self.proxy_page_urls)
        if  pages_num <= 0:
            return
        
        pool = multiprocessing.Pool(processes=pages_num)
        results = []
        for pageurl in self.proxy_page_urls:        
            proxies_page = self._scrape_single_page_proxies(pageurl)
            results.append(pool.apply_async(_test_proxies, (proxies_page, )))                 
        pool.close()
        pool.join()
        for res in results:
            valid_proxies.extend(res.get())
        print len(valid_proxies)
        with open("proxies_%s.txt"%self.proxy_website,"w+") as f:
            f.write(simplejson.dumps(valid_proxies))

if __name__ == "__main__":
    proxy = theproxy()
    proxy.ip = "222.74.28.14"
    proxy.port = 23
    proxy.protocol = "http"
    _test_proxy(proxy)

   
                   
            
