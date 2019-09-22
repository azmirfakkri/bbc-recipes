# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from datetime import datetime


class RecipesItem(scrapy.Item):
    recipe_id_nk = scrapy.Field()
    title = scrapy.Field()
    recipe_description = scrapy.Field()
    recipe_url = scrapy.Field()
    recipe_type = scrapy.Field()
    prep_time = scrapy.Field()
    cooking_time = scrapy.Field()
    serves = scrapy.Field()
    dietary = scrapy.Field()
    methods = scrapy.Field()
    ingredients = scrapy.Field()
    inserted_at = scrapy.Field(serializer=datetime)


class RawIngredientsItem(scrapy.Item):
    raw_id = scrapy.Field()
    raw_ingredient = scrapy.Field()
    inserted_at = scrapy.Field(serializer=datetime)

