import scrapy

gnumber = 0

class Googreads_quotes(scrapy.Spider):
	name = "ganji_rent"
	start_urls = ['http://sh.ganji.com/xiaoqu/xinkaijiayuan/chuzufang/f0/', ]
	

	def parse(self, response):
		global gnumber

		with open("ganji_rent.txt", "a") as f:
				f.write('------------------------Page {0}-------------------------\n\n'.format(gnumber+1))
				f.close()

		for house in response.css('dl.list-img'):
			try:
				housesdict = { 
					'house-desc': house.css('div.info-title a::text').extract_first(), 
					'house-addr': house.css('p.list-word a::text').extract(), 
					'house-lane': house.css('p.list-word::text')[2].extract(),
					'house-type': house.css('p.list-word::text')[3].extract().replace('\n', ''), 
					'house-price': house.css('span.price b.fc-org::text').extract_first() + house.css('span.price::text').extract_first(), 
					'house-pubtime': house.css('span.pubtime::text').extract_first(),
				}
				#print(quotesdict['text'] + "------------------")
				with open("ganji_rent.txt", "a") as f:
					f.write(housesdict['house-desc'] + '\n')
					f.write('-'.join(housesdict['house-addr']) + '\t')
					f.write(housesdict['house-lane'] + '\n')
					f.write(housesdict['house-type'] + '\n')
					f.write(housesdict['house-price'] + '\n')
					f.write(housesdict['house-pubtime'] + '\n')
					f.write('\n\n')
					f.close()
			except Exception as e:
				print(housesdict['house-desc'])
			finally:
				yield housesdict
			
		next_page = response.css('div.pageBox a.next::attr(href)').extract_first()
		#print('+++++++++++++++++++' + next_page)
		
		gnumber += 1
		if (next_page is not None): 
			next_page = response.urljoin(next_page) 
			#print(next_page)
			yield scrapy.Request(next_page, callback=self.parse)