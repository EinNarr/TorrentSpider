import scrapy

from TorrentSpider.items import TorrentItem

class TorrentSpider(scrapy.Spider):
    name = "TorrentSpider"
    allowed_domains = ["put_a_torrent_discovery_website_here"]
    start_urls = [
        "https://" + allowed_domains[0] + "/top/200"
    ]
    current = 0
    top = []

    def parse(self, response):
        self.top = response.xpath('//*[@id="searchResult"]/tr/td[2]/div/a/@href').extract()
        url = "https://" + self.allowed_domains[0] + self.top[self.current]
        yield scrapy.Request(url, callback=self.parse_TPB, errback=self.errback)


    def parse_TPB(self, response):
        item = TorrentItem()
        details = response.xpath('/html/body/div[@id="content"]/div[@id="main-content"]/div/div[@id="detailsouterframe"]/div[@id="detailsframe"]/div[@id="details"]')
        item["title"] = details.xpath('../div[@id="title"]/text()').extract()[0].strip()
        item["link"] = "https:" + response.xpath('/html/head/link[@rel="canonical"]/@href').extract()[0]
        item["magnet_link"] = details.xpath('./div/div[@class="download"]/a[@title="Get this torrent"]/@href').extract()[0]
        item["size"] = int(details.xpath('./dl[@class="col1"]/dd[3]/text()').extract()[0].split("(")[1].split("Bytes")[0].strip())   # in Bytes
        # item["time"] = details.xpath('./dl[@class="col2"]/dd[1]/text()').extract() or details.xpath('./dl[@class="col1"]/dd[8]/text()').extract()
        # item["time"] = item["time"][0]
        # item["seed"] = details.xpath('./dl[@class="col2"]/dd[3]/text()').extract() or details.xpath('./dl[@class="col1"]/dd[10]/text()').extract()
        # item["seed"] = int(item["seed"][0])
        # item["leech"] = details.xpath('./dl[@class="col2"]/dd[4]/text()').extract() or details.xpath('./dl[@class="col1"]/dd[11]/text()').extract()
        # item["leech"] = int(item["leech"][0])

        yield item

        print self.current
        print len(self.top)
        self.current += 1

        if self.current<100:
            url = "https://" + self.allowed_domains[0] + self.top[self.current]
            yield scrapy.Request(url, callback=self.parse_TPB, errback=self.errback)
    
    def errback(self, error):
        url = "https://" + self.allowed_domains[0] + self.top[self.current]
        yield scrapy.Request(url, callback=self.parse_TPB, errback=self.errback)
