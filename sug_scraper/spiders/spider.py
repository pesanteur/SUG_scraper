from scrapy import Spider


class SUGSpider(Spider):

    name = "SUG"
    allowed_domains = ["signupgenius.com"]

    def parse(self, response):
        #TODO: tidy this up and make it more generalized
        log.msg('parse(%s)' % response.url, level = log.DEBUG)
        rows = response.xpath('//table[@class="SUGtableouter"]/tr')
        for row in rows:
            item = ScheduleItem()
            item['Date'] = response.xpath('/tr[2]/td/span/text()').extract()[0] #first row of tables
            item['Location'] = response.xpath('/tr[2]/td/span/text()').extract()[1]
            item['Time'] = response.xpath('/tr[2]/td/span/text()').extract()[2]
            item['DES Group'] = response.xpath('/tr[2]/td/table/tr/td/span/text()').extract() #sub table in first row
            item['Status'] = response.xpath('/tr[2]/td/table/tr/td[3]/div/span/span/text()').extract() #sign up/already filled
        for row in rows:
            item['Date'] = row.xpath('td/span/text()').extract()[0]
            item['Location'] = row.xpath('td/span/text()').extract()[1]
            #item['Time'] = row.xpath('td/span/text()').extract()[2]
            item['DES Group'] = row.xpath('td/table/tr/td/span/text()').extract()[0]
            item['Status'] = row.xpath('td/table/tr/td/div/span/span/text()').extract()
            #TODO: check if status is empty if it is check for "Already filled"
            item['Status'] = row.xpath('td/table/tr/td/div/span/text()').extract()
