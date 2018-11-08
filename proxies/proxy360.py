from getproxies import *
import requests

class proxy360scraper(proxyscraper):
    def __init__(self):
        proxyscraper.__init__(self)
        self.baseurl = "http://www.proxy360.net"
        self.category = ""
    def build_proxy_page_urls(self):
        r = requests.get("%s/%s/"%(self.baseurl,self.category))
        response = r.text
        tree = lxml.html.fromstring(response)
        sel = CSSSelector('div.pagination li a')
        rows = sel(tree) 
        page = 0
        for row in rows:
            try:
                if page < int(row.text_content()):
                    page = int(row.text_content())
            except Exception,e:
                continue
        self.proxy_page_urls = ["%s/%s/%d"%(self.baseurl,self.category,p) for p in range(1,page+1) ]

    def _parse_response(self, response):
        tree = lxml.html.fromstring(response)
        sel = CSSSelector('#listtable tbody tr')
        col_sel = CSSSelector('td')
        style_sel = CSSSelector('style')
        span_sel = CSSSelector('span')
        speed_sel = CSSSelector('.progress-indicator div')

        rows = sel(tree)  
        proxies = []
        for row in rows:
            cols = col_sel(row)

            if len(cols) < 7:
                continue
            #cols[1]: ip
            #cols[2]: port
            #cols[3]: Country
            #cols[4]: speed
            #cols[6]: protocol
            p = theproxy()    
            
            styles = style_sel(cols[1])

            invisible_style = [string.replace(style,'{display:none}','').replace('.','') for style in string.split(styles[0].text_content()) if style.find('display:none') <> -1]          
                    
            elems = cols[1].find('span')      

            ip = ''
            for elem in list(elems):
                if elem.tag == 'style':
                    elem.text = ""
                if elem.tag == 'div' or elem.tag == 'span':
                    if 'style' in elem.attrib and elem.attrib['style'] == 'display:none':
                        elem.text = ""
                    if 'class' in elem.attrib and elem.attrib['class'] in invisible_style:
                        elem.text = ""

            p.ip = elems.text_content().strip()
            p.port = int(cols[2].text_content().strip())
            p.country = cols[3].attrib['rel'].strip()
            
            speed_str = lxml.html.tostring(cols[4])
            
            speed_re = re.compile(".*width: ([0-9]+)%.*")
            m_result = speed_re.match(speed_str)

            p.speed = int(m_result.group(1))
            p.protocol = cols[6].text_content().strip().lower()
            proxies.append(p)

        return proxies

class proxy360guoneiscraper(proxy360scraper):
    def __init__(self):
        proxy360scraper.__init__(self)
        self.category = "guonei"
        self.proxy_website = "proxy360.net.guonei"

class proxy360guowaiscraper(proxy360scraper):
    def __init__(self):
        proxy360scraper.__init__(self)
        self.category = "guowai"
        self.proxy_website = "proxy360.net.guowai"


if __name__ == "__main__":
    ps = proxy360guoneiscraper()
    ps.scrape_proxies()
    ps = proxy360guowaiscraper()
    ps.scrape_proxies()