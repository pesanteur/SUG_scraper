from scrapy import Spider
from scrapy import log
from sug_scraper.items import SugScraperItem

class SUGSpider(Spider):
    name = "SUG"
    allowed_domains = ["signupgenius.com"]
    start_urls = ('http://www.signupgenius.com/go/10c084baaa82da2fe3-term227',)

    def parse(self, response):
        #TODO: tidy this up and make it more generalized
        log.msg('parse(%s)' % response.url, level = log.DEBUG)
        rows = response.xpath('//table[@class="SUGtableouter"]/tr')
        """
        for row in rows:
            item['Date'] = response.xpath('/tr[2]/td/span/text()').extract()[0] #first row of tables
            item['Location'] = response.xpath('/tr[2]/td/span/text()').extract()[1]
            item['Time'] = response.xpath('/tr[2]/td/span/text()').extract()[2]
            item['DES_Group'] = response.xpath('/tr[2]/td/table/tr/td/span/text()').extract() #sub table in first row
            item['Status'] = response.xpath('/tr[2]/td/table/tr/td[3]/div/span/span/text()').extract() #sign up/already filled
        """
        for row in rows:
            #TODO: Don't need a for loop creates errors fix this
            item = SugScraperItem()
            #item['Date'] = row.xpath('td/span/text()').extract()[0]
            #item['Location'] = row.xpath('td/span/text()').extract()[1]
            item['Time'] = row.xpath('td[1]/span/text()').extract()
            item['DES_Group'] = row.xpath('td/table/tr/td/span[@class="SUGbigbold"]/text()').extract()
            item['Topic'] = row.xpath('td/table/tr/td/span[@class="SUGcomment"]/text()').extract()
            item['Status'] = row.xpath('td/table/tr/td/div/span/span/text()').extract()
            #TODO: check if status is empty if it is check for "Already filled"
            #item['Status'] = row.xpath('td/table/tr/td/div/span/text()').extract()
            yield item
