# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from time import sleep


class BbcRecipesSpider(scrapy.Spider):
    name = 'bbc_recipes'
    allowed_domains = ['bbc.co.uk']
    start_urls = ['https://www.bbc.co.uk/food/recipes/a-z/a/1#featured-content']

    BASE_URL = 'https://www.bbc.co.uk'

    def parse(self, response):
        sleep(2)
        # get all the recipe links after the page is loaded
        recipe_links = response.xpath("//a[contains(@class, 'promo')]/@href").extract()

        # follow every recipe link and scrape the content
        for recipe_link in recipe_links:
            absolute_url = self.BASE_URL + recipe_link
            yield scrapy.Request(absolute_url, callback=self.parse_result)

        # get the list of hrefs for next page
        next_hrefs = response.xpath("//a[@class='pagination__link gel-pica-bold']/@href").extract()
        for next_href in next_hrefs:
            next_page_url = self.BASE_URL + next_href
            yield scrapy.Request(url=next_page_url)

    def parse_result(self, response):
        doc_title = response.body_as_unicode()
        soup = BeautifulSoup(doc_title, 'html.parser')

        # get recipe
        title = soup.find('h1', class_="gel-trafalgar content-title__text").text

        try:
            recipe_description = soup.find('p', class_="recipe-description__text").text
        except:
            recipe_description = "NA"

        print(recipe_description)
        print(title)
