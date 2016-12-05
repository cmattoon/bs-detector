# -*- coding: utf-8 -*-
import scrapy, re
from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.shell import inspect_response

xpaths = {
    'conspiracy':'//*[@id="post-50"]/div/p[2]/a/@href',
    'satire':'//*[@id="post-48"]/div/p[2]/a/@href',
    'left':'//*[@id="post-37"]/div/p[2]/a/@href',
    'right':'//*[@id="post-46"]/div/p[2]/a/@href',
    }

class MediabiasfactcheckSpider(CrawlSpider):
    name = "mediabiasfactcheck"
    allowed_domains = ["mediabiasfactcheck.com"]
    start_urls = (
        'http://www.mediabiasfactcheck.com/left/',
        'http://www.mediabiasfactcheck.com/right/',
        'http://www.mediabiasfactcheck.com/conspiracy/',
        'http://www.mediabiasfactcheck.com/satire/',
    )

    rules = (
        Rule(
            LxmlLinkExtractor(
                restrict_xpaths=xpaths.values(),
                ),
            follow=True
            ),
        )


    def parse(self, response):
        print("\033[92m")
        print("Parsing....")
        print("\033[0m")
        for tag in xpaths.keys():
            elements = response.xpath(xpaths[tag])
            if len(elements):
                print("\033[32m")
                print("Found %d for %s" % (len(elements), tag))
                print elements
                print("\033[0m")
                for el in elements:
                    url = el.extract()
                    print("\033[95m %s\033[0m" % (str(url)))
                    yield Request(url,
                                  callback=self.parse_page)
    def parse_page(self, response):
        """This is ugly"""
        url = ''
        reason = response.xpath('//*/div/header/h1/text()').extract()
        reason = str(reason[0])
        idx = response.body.find('Source:')
        if idx: # should never be zero
            txt = response.body[idx:idx+100] # should be enough
            m = re.search(r'href=[\'"]?([^\'">]+)', txt)
            if m:
                url = m.group(1)

        if url and reason:
            with open('urls.txt', 'a') as fd:
                print("\033[94m<%s> (%s)\033[0m" % (str(url), str(reason)))
                fd.write("%s,%s\n" % (str(url), str(reason)))

