# -*- coding: cp936 -*-

import settings
import requests

def vote(proxy):
    for i in range(5):
        try:
            r = requests.post('http://active.cnjxol.com/votenet/4thfyrw?cate=4',
                timeout=5, 
                data = {"pids":"85","submit":"提交投票"}, 
                headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'},
                proxies = {"http": '%s:%d'%(proxy["ip"],proxy["port"])})
            if r.status_code == 200:
                print "vote successfully"
                break
            else:
                print "vote failed"
        except:
            print "vote failed"


if __name__ == "__main__":
    vote({"protocol":"http", "ip":"183.207.228.9","port":80})
    
    