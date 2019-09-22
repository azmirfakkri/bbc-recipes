# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from time import sleep
from datetime import datetime

from ..items import RecipesItem, RawIngredientsItem


class BbcRecipesSpider(scrapy.Spider):
    name = 'bbc_recipes'
    allowed_domains = ['bbc.co.uk']
    start_urls = ['https://www.bbc.co.uk/food/recipes/a-z/a/1#featured-content']

    BASE_URL = 'https://www.bbc.co.uk'

    def parse(self, response):
        sleep(2)
        # get all the recipe href after the page is loaded
        recipe_hrefs = response.xpath("//a[contains(@class, 'promo')]/@href").extract()

        try:
            recipe_types = response.xpath("//span[@class='promo__type gel-minion' or @class='promo__type gel-minion no-image']/text()").extract()
        except:
            recipe_types = "NA"

        list_of_tuples = list(zip(recipe_hrefs, recipe_types))

        # follow every recipe link and scrape the content
        for recipe_href, recipe_type in list_of_tuples:
            absolute_url = self.BASE_URL + recipe_href
            yield scrapy.Request(absolute_url, callback=self.parse_result, meta={'recipe_type': recipe_type})

        # for recipe_href in recipe_hrefs:
        #     absolute_url = self.BASE_URL + recipe_href
        #     yield scrapy.Request(absolute_url, callback=self.parse_result)

        # get the list of hrefs for next page
        next_hrefs = response.xpath("//a[@class='pagination__link gel-pica-bold']/@href").extract()
        for next_href in next_hrefs:
            next_page_url = self.BASE_URL + next_href
            yield scrapy.Request(url=next_page_url)

    def parse_result(self, response):
        doc_title = response.body_as_unicode()
        soup = BeautifulSoup(doc_title, 'html.parser')

        try:
            title = soup.find('h1', class_="gel-trafalgar content-title__text").text
        except:
            title = "NA"

        try:
            recipe_description = soup.find('p', class_="recipe-description__text").text
        except:
            recipe_description = "NA"

        try:
            prep_time = soup.find('p', class_="recipe-metadata__prep-time").text
        except:
            prep_time = "NA"

        try:
            cooking_time = soup.find('p', class_="recipe-metadata__cook-time").text
        except:
            cooking_time = "NA"

        try:
            serves = soup.find('p', class_="recipe-metadata__serving").text
        except:
            serves = "NA"

        try:
            dietary = soup.find('p', class_="recipe-metadata__dietary-vegetarian-text").text
        except:
            dietary = "NA"

        try:
            methods_list = []
            method_elements = soup.find_all('p', class_="recipe-method__list-item-text", text=True)
            for method_element in method_elements:
                method_text = method_element.get_text()
                methods_list.append(method_text)
            methods = ' '.join(methods_list)
        except:
            methods = "NA"

        try:
            ingredients_list = []
            ingredient_elements = soup.find_all('li', class_="recipe-ingredients__list-item")
            for ingredient_element in ingredient_elements:
                ingredient_text = ingredient_element.get_text()
                ingredients_list.append(ingredient_text)
            ingredients = '\n'.join(ingredients_list)
        except:
            ingredients = "NA"

        # TODO: need to extract only raw ingredients from ingredients

        recipe = RecipesItem()
        recipe['title'] = title
        recipe['recipe_description'] = recipe_description
        recipe['recipe_url'] = response.request.url
        recipe['recipe_type'] = response.meta.get('recipe_type')
        recipe['recipe_description'] = recipe_description
        recipe['prep_time'] = prep_time
        recipe['cooking_time'] = cooking_time
        recipe['serves'] = serves
        recipe['dietary'] = dietary
        recipe['methods'] = methods
        recipe['ingredients'] = ingredients

        now = datetime.now()
        date_str = now.strftime("%d-%m-%y %H:%M:%S")
        recipe['inserted_at'] = date_str

        yield recipe

        ingredient = RawIngredientsItem()
        ingredient['raw_ingredient'] = ingredients  # TODO: need to extract only raw ingredients from ingredients
        ingredient['inserted_at'] = date_str

        yield ingredient
