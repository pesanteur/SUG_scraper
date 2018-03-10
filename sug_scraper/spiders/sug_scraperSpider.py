import requests
import logging
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy import Spider
from sug_scraper.items import SugScraperItem
from scrapy.http import Request

class SUGSpider(Spider):
    name = "sug_scraperSpider"
    allowed_domains = ["signupgenius.com"]
    start_urls = ('http://www.signupgenius.com/go/10c084baaa82da2fe3-term247',)
    base_table = '//table[@class="SUGtableouter"]/tr'
    """
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.basicConfig(
            level=logging.DEBUG,
            format =
            '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
            datefmt='%a, %d %b % Y %H:%M:%S',
            filename='cataline.log',
            filemode='w')
    """
    def parse(self, response):
        #log.msg('parse(%s)' % response.url, level = log.DEBUG)
        rows = response.xpath('//table[@class="SUGtableouter"]/tr[position()>1]')

        count = 0
        actual_date = 0
        for row in rows:
            item = SugScraperItem()
            date = row.xpath('td[1]/span/text()').extract()
            if "2018" in date[0]:
                actual_date = date[0]
                day = row.xpath('td[2]/span/text()').extract()
                day = self.trim(day[0])
                real_date = actual_date, day
                item['Time'] = real_date
                continue
            else:
                day = self.trim(date[0])
                real_date = actual_date, day
                item['Time'] = real_date
            #item['Time'] = row.xpath('td/span/text()').extract()
            # NOTE: des_group is a row to itself, so have to navigate that as well
            des_column = row.xpath('td/table/tr/td/p[1]/text()').extract()
            for des_group in des_column:
                item['DES_Group'] = des_group
                #TODO: align DEs group to time slot and time...how?
            #item['DES_Group'] = [i.replace('\t', '') for i in des_group]
            #item['Status'] = row.xpath('td/table/tr/td/div/span/span/text()').extract()
            #TODO: check if status is empty if it is check for "Already filled"
            #item['Status'] = row.xpath('td/table/tr/td/div/span/text()').extract()
            already_filled = row.xpath('td/table/tr/td/div/span[not(@class="SUGbutton rounded")]/text()').extract() # This xpath ignores button text to provide sanitized data
            sign_up = row.xpath('td/table/tr/td/div/span/span/text()').extract()
            sign_up = [self.trim(i) for i in sign_up]
            if already_filled:
                for i in already_filled:
                    if '\n' in i:
                        continue
                    else:
                        item['Status'] = already_filled
            else:
                item['Status'] = sign_up
            yield item


#TODO: Fix these, these two just reposts the first
    def get_status(self, response):
        status = response.xpath('//table[@class="SUGtableouter"]/tr/td/table/tr/td/div/span/text()').extract()[0]
        return self.trim(status)

    def get_group(self, response):
        path = self.base_table + '/'
        new_path = path + 'td/table/tr/td/span[1]/text()' # this is gross...don't do this
        des_group = response.xpath(new_path).extract()
        trim_des = [i.replace('\t', '') for i in des_group]
        return trim_des

    def trim(self, raw_string):
        return raw_string.encode('ascii', errors='ignore').strip()

    def check_if_date():
        pass

    def text_cleanup(self, raw_string):
        return raw_string.replace('\t', '')
