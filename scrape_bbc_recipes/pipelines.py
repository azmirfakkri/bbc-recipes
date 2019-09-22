# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import DataError, IntegrityError
from . models import Recipe, RawIngredient, db_connect, create_table
from . items import RecipesItem, RawIngredientsItem
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
        Dump recipes into the db
        """
        if isinstance(item, RecipesItem):
            return self.process_recipe(item, spider)
        if isinstance(item, RawIngredientsItem):
            return self.process_raw_ingredient(item, spider)

    def process_recipe(self, item, spider):
        # parse the date
        item['inserted_at'] = datetime.strptime(item['inserted_at'], "%d-%m-%y %H:%M:%S")

        # get the recipe id
        item['recipe_id_nk'] = item['recipe_url'].split('_')[-1]

        session = self.Session()
        recipe = Recipe(**item)

        try:
            session.add(recipe)
            session.commit()
        except DataError as error:
            log.exception(error)
        except IntegrityError:
            session.rollback()
            session.merge(recipe)
            session.commit()

    def process_raw_ingredient(self, item, spider):
        # parse the date
        item['inserted_at'] = datetime.strptime(item['inserted_at'], "%d-%m-%y %H:%M:%S")

        session = self.Session()
        raw_ingredient = RawIngredient(**item)

        # TODO: dump each raw ingredient as a single entry in raw_ingredient table

        try:
            session.add(raw_ingredient)
            session.commit()
        except DataError as error:
            log.exception(error)
        except IntegrityError:
            session.rollback()
            session.merge(raw_ingredient)
            session.commit()
