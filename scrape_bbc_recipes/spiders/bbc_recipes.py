# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup


class BbcRecipesSpider(scrapy.Spider):
    name = 'bbc_recipes'
    allowed_domains = ['bbc.co.uk']
    start_urls = ['https://www.bbc.co.uk/food/recipes/a-z/a/1#featured-content']

    BASE_URL = 'https://www.bbc.co.uk'

    def parse(self, response):
        recipe_links = response.xpath("//a[contains(@class, 'promo')]/@href").extract()

        for recipe_link in recipe_links:
            absolute_url = self.BASE_URL + recipe_link
            yield scrapy.Request(absolute_url, callback=self.parse_result())

    def parse_result(self, response):
        doc_title = response.body_as_unicode()
        soup = BeautifulSoup(doc_title, 'html.parser')

        # get recipe
        recipe = soup.find_all('a', class_="promo")

