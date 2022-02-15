from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup
import re


class EtWikiCrawler(CrawlSpider):
    name = 'TheFriendlyNeighbourhoodSpider'

    allowed_domains = ['et.wikipedia.org']
    start_urls = ['https://et.wikipedia.org/wiki/Vabadussõda', ]

    custom_settings = {
        'LOG_LEVEL': 'INFO',
        'FEED_EXPORT_ENCODING': 'utf-8',
    }

    rules = (
        Rule(LinkExtractor(
            deny=['/Kategooria', 'action=edit', '/Fail', '/Vikipeedia:', '/Mall', '/Juhend', '/Arutelu:', '/Eri:'],
            allow='/wiki', restrict_css="div.mw-parser-output"),
            callback='parse_item',
            follow=True),
    )

    def parse_item(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        # Sõna
        name = soup.find(id="firstHeading").text
        name = re.sub("\s*\(.*\)\s*", "", name)

        # Definitsioon
        defi = soup.find("div", class_="mw-parser-output")
        if defi:
            res = defi.find("p", recursive=False)
            if res:
                res = res.text
                res = re.search("(?<=\son\s).*|(?<=\soli\s).*|(?<=\stoimus\s).*", res)
                if res:
                    res = res.group()
                    res = re.sub("\[.*?\]", "", res)
                    #Väljasta
                    yield {
                        'name': name,
                        'def': res,
                    }
