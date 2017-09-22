import urllib2
import urlparse
import datetime
import time
# three ways to match date on the web and get it
import re
from bs4 import BeautifulSoup
import lxml.html   #  this way is the best performance

class Throttle:
    """Add a delay between downloads to the same domain"""
    def __init__(self, delay):
        self.delay = delay
        self.domains = {}

    def wait(self, url):
        domain = urlparse.urlparse(url).netloc
        last_accessed = self.domains.get(domain)

        if self.delay > 0 and last_accessed is not None:
            sleep_secs = self.delay - (datetime.datetime.now() - last_accessed).seconds
            if sleep_secs > 0:
                time.sleep(sleep_secs)
        # Update the last accessed recently
        self.domains[domain] = datetime.datetime.now()



def download(url, user_agent='wswp', proxy=None, num_retries=2):
    """catch web content"""
    print "Downloading:'", url, "' Now"
    headers = {'User-agent': user_agent}
    request = urllib2.Request(url, headers=headers)

    # using urllib2 agent
    opener = urllib2.build_opener()
    if proxy:
        proxy_params = {urlparse.urlparse(url).scheme:proxy}
        opener.add_handler(urllib2.ProxyHandler(proxy_params))
    try:
        html = opener.open(request).read()
    except urllib2.URLError as e:
        print 'Download Error:', e
        html = None
        if num_retries>0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                # retry 2 times if 5XX errors
                return download(url, user_agent, num_retries-1)
    return html

def crawl_sitemap(url):
    """get web map information,if you want to test this function,use this url:http://example.webscraping.com/places/default/sitemap.xml"""
    sitemap = download(url)
    links = re.findall('<loc>(.*?)</loc>', sitemap)
    for link in links:
        print link

def link_crawler(seed_url, link_regex, max_depth=2):
    """Crawl from the given seed_url following links matched by link_regex
    It can also avoid crawling duplicate web pages"""
    crawl_queue=[seed_url]
    seen = {}
    link_regex = re.compile(link_regex)
    #delay some secs
    throttle = Throttle(2)
    while crawl_queue:
        url = crawl_queue.pop()
        throttle.wait(url)
        html = download(url)
        # Limit crawler depth to avoid the crawler trap.But pay attention,this logic will change with the change of the website structure
        if seen.get(url):
            depth = seen[url]
        else:
            seen[url] = depth = 0
        if depth != max_depth:
            for link in get_links(html):
                # check if link matches expected regex
                if re.match(link_regex, link):
                    # Form absolute link
                    # If the link is relative link,the combination should be prohibited
                    link = urlparse.urljoin(seed_url, link)
                    if link not in seen.keys():
                        seen[link] = depth+1
                        crawl_queue.append(link)

def get_links(html):
    """Return all links in html"""
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    return webpage_regex.findall(html)





if __name__ == '__main__':
    link_crawler("http://example.webscraping.com", '/places/default/(index|view)')


