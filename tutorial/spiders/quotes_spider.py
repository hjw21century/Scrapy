'''
import scrapy

class QuotesSpider(scrapy.Spider):
	name = "quotes"

	def start_requests(self):
		urls = [ 'http://quotes.toscrape.com/page/1/', 'http://quotes.toscrape.com/page/2/', ] 
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		page = response.url.split("/")[-2] 
		filename = 'quotes-%s.html' % page 
		with open(filename, 'wb') as f:
			f.write(response.body)
			self.log('Saved file %s' % filename)
'''

import scrapy

class QuotesSpider(scrapy.Spider):
	name = "quotes"
	start_urls = ['http://quotes.toscrape.com/page/1/', ]

	def parse(self, response):
		for quote in response.css('div.quote'):
			quotesdict = { 
				'text': quote.css('span.text::text').extract_first(), 
				'author': quote.css('span small::text').extract_first(), 
				'tags': quote.css('div.tags a.tag::text').extract(), 
			}
			#print(quotesdict['text'] + "------------------")
			with open("quoteslist.txt", "a") as f:
				f.write(quotesdict['text'] + '\t')
				f.write('----' + quotesdict['author'])
				#f.write(', '.join(quotesdict['tags'])
				f.write('\n\n\n')
				f.close()
			yield quotesdict
		next_page = response.css('li.next a::attr(href)').extract_first() 
		print('+++++++++++++++++++' + next_page)
		if next_page is not None: 
			next_page = response.urljoin(next_page) 
			yield scrapy.Request(next_page, callback=self.parse)
