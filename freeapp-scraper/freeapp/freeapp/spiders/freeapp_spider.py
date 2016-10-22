import scrapy
from scrapy.selector import HtmlXPathSelector

from stackoverflow.items import AppItem

class AppleSpider(scrapy.Spider):
    name = "apple"
    allowed_domains = ["apple.com"]
    start_urls = ["http://www.apple.com/itunes/charts/free-apps/"]

    def parse(self, response):
    	hxs = scrapy.Selector(response)
    	apps = hxs.css('div.section-content')[1].css('li')
    	count = 0
    	items = []

    	for app in apps:
    		item = AppItem()
    		item['app_name'] = app.css('h3 a::text').extract_first()
    		item['appstore_link'] =  app.css('h3 a::attr(href)').extract_first()
    		item['category'] = app.css('h4 a::text').extract_first()
    		item['img_src'] = app.css('h4 a::attr(href)').extract_first()

    		items.append(item)
    		count += 1

    	return items