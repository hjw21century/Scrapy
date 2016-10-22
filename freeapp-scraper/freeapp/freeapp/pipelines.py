import json

import datetime

import MySQLdb

from scrapy.exceptions import DropItem
from scrapy.conf import settings

IFILE = 'items.json'
indexes=0

def format_location(s):
    return s.strip()


def format_description(l):
    l = map(lambda s: s.strip(), l)
    l = filter(lambda s: s, l)
    return l  # returns a list of cleaned non empty phrases


class FormatPipeline(object):

    def process_item(self, item, spider):
        item['location'] = format_location(item['location'])
        item['description'] = format_description(item['description'])
        return item


class MySQLdbPipeline(object):

    def __init__(self):
        connection = MySQLdb.connect(
            user="root",
            passwd="",
            db="stackoverf"
        )
        c=connection.cursor()

    def process_item(self, item, spider):
        # upsert to insert if id not found,
        # otherwise update date_updated to be now
        # date_updated will last have the last date the job was online
        date_updated = datetime.datetime.now()
        columns = ['id', 'title', 'tags', 'date', 'location', 'employer', 'description', 'url']
        insert_statment = 'INSERT INTO job_item(%s) values(%s)'.format(','.join(columns),','.join(['%s']*len(columns)))
        global indexes
        indexes += 1
        c.executemany(insert_statment,  
        [
        (indexes,item[columns[1]],item[columns[2]],item[columns[3]],item[columns[4]],item[columns[5]],item[columns[6]],item[columns[7]])
        ])
        connection.commit()

        return item


class MySQLdbPipeline2(object):

    def __init__(self):
        self.connection = MySQLdb.connect(
            user="root",
            passwd="",
            db="stackoverf"
        )
        self.c = self.connection.cursor()

    def process_item(self, item, spider):

        columns = ['app_name', 'category', 'appstore_link', 'img_src']
        insert_statment = 'INSERT INTO job_item({0}) values({1})'.format(','.join(columns),','.join(['%s']*len(columns)))
        global indexes
        indexes += 1

        self.c.executemany(insert_statment,  
        [
        (item[columns[0]],item[columns[1]],item[columns[2]],item[columns[3]]),
        ])
        self.connection.commit()

        return item


class DuplicatesPipeline(object):

    ids = []
    with open(IFILE,'r') as f:
        for line in f:
            item = json.loads(line.strip())
            ids.append(item['id'])

    def process_item(self, item, spider):
        if item['id'] in self.ids:
            raise DropItem("Item already crawled")
        else:
            return item


class JsonWriterPipeline(object):

    def __init__(self):
        self.ifile = open(IFILE, 'a')

    def process_item(self, item, spider):
        item = dict(item)
        iline = json.dumps(item) + "\n"
        self.ifile.write(iline)
        return item
