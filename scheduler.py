import settings
import proxies.scraperloader
import myproxy
import voter
import time
import sys
import random
import datetime

def run(flag):
    if flag <> '-l':
       proxies.scraperloader.load_scraper()

    myproxy.load_proxy()
    
    proxy_nums = myproxy.proxy_nums()
    print "%d proxies loaded"%proxy_nums

    available_votes = proxy_nums * settings.MAX_VOTE_PER_IP

    interval = 1.0 * settings.TOTAL_TIME / available_votes

    vote_no = 0

    while True:
        now = datetime.datetime.now()
        if (now.hour >= 22 and now.hour <= 23) or (now.hour >= 0 and now.hour <= 7):
            time.sleep(1800)
            continue
        p = myproxy.get_one_proxy()
        if len(p) == 0:
            print "out of proxy!"
            break
        voter.vote(p)
        vote_no = vote_no + 1
        next_inteval = random.randint(2,int(interval*2))
        print "Vote:%d done with %s! Wait %d ms for next vote"%(vote_no,p["ip"].decode('utf-8').encode('gb2312'),next_inteval*1000)
        time.sleep(next_inteval)


if __name__ == "__main__":
    flag = ""
    if len(sys.argv) > 1:
        flag = sys.argv[1]
    run(flag)