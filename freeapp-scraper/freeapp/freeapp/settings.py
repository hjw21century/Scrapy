# -*- coding: utf-8 -*-

# Scrapy settings for stackoverflow project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#


DOWNLOAD_DELAY = 0.5


ITEM_PIPELINES = {
    'freeapp.pipelines.MySQLdbPipeline2': 200,
    'freeapp.pipelines.DuplicatesPipeline': 300,
    'freeapp.pipelines.JsonWriterPipeline': 500,
}
