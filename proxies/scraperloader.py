#!/usr/bin/python
from proxy360 import proxy360guoneiscraper
from proxy360 import proxy360guowaiscraper
from proxycomru import proxydotcomscraper

def load_scraper():
    for i in range(10):
        try:
            ps = proxydotcomscraper()
            ps.scrape_proxies()
            ps = proxy360guoneiscraper()
            ps.scrape_proxies()
            ps = proxy360guowaiscraper()
            ps.scrape_proxies()
            break
        except Exception:
            pass

if __name__ == "__main__":
    load_scraper()