# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import DataError, IntegrityError
from . models import Recipes, db_connect, create_table
from datetime import datetime
from logging import getLogger

log = getLogger(__name__)


class ScrapeBbcRecipesPipeline(object):
    def __init__(self):
        """
        Initializes pipeline for storing scraped items in the database
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """
        Dump ad into the db
        """
        # parse the date
        item['last_seen'] = datetime.strptime(item['last_seen'], "%d-%m-%y %H:%M:%S")

        if 'first_seen' in item.keys():
            item.pop('first_seen')

        session = self.Session()
        ad = Recipes(**item)

        try:
            session.add(ad)
            session.commit()
        except DataError as error:
            log.exception(error)
        except IntegrityError:
            session.rollback()
            session.merge(ad)
            session.commit()
