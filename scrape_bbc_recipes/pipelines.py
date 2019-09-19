# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import DataError, IntegrityError


class ScrapeBbcRecipesPipeline(object):
    def process_item(self, item, spider):
        return item
