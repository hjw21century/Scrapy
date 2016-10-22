# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class AppItem(scrapy.Item):

	# define the fields for your item here like:
	app_name = Field()
	category = Field()
	appstore_link = Field()
	img_src = Field()