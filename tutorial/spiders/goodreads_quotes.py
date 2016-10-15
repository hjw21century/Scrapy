import scrapy

gnumber = 0

class Googreads_quotes(scrapy.Spider):
	name = "googreads_quotes"
	start_urls = ['https://www.goodreads.com/quotes?page=1', ]

	def parse(self, response):
		global gnumber

		with open("googreads_quotes.txt", "a") as f:
				f.write('------------------------List {0}-------------------------\n\n'.format(gnumber+1))
				f.close()

		for quote in response.css('div.quoteDetails'):
			quotesdict = { 
				'text': quote.css('div.quoteText::text').extract_first(), 
				'author': quote.css('div.quoteText a.authorOrTitle::text').extract_first(), 
				'tags': quote.css('div.quoteFooter div.greyText a::text').extract(), 
			}
			#print(quotesdict['text'] + "------------------")
			with open("googreads_quotes.txt", "a") as f:
				f.write(quotesdict['text'] + '\t\t\t')
				f.write('----' + quotesdict['author'])
				#print(', '.join(quotesdict['tags']) + '....................')
				f.write('\n\t\t\ttags: ' + ', '.join(quotesdict['tags']))
				f.write('\n\n\n')
				f.close()
			yield quotesdict
		next_page = response.css('.next_page::attr(href)').extract_first() 
		#print('+++++++++++++++++++' + next_page)
		
		gnumber += 1
		if (next_page is not None and gnumber < 100): 
			next_page = response.urljoin(next_page) 
			#print(next_page)
			yield scrapy.Request(next_page, callback=self.parse)