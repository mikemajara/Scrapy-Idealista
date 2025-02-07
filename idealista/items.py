# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class IdealistaItem(scrapy.Item):
    #Matching variables of every flat to be scrapped
    #id_idealista = scrapy.Field()
    date = scrapy.Field()
    link = scrapy.Field()
    price = scrapy.Field()
    address = scrapy.Field()
    sqft_m2 = scrapy.Field()
    rooms = scrapy.Field()
    discount = scrapy.Field()
    floor_elevator = scrapy.Field()

    def to_json(self):
        return dict(
            date=self['date'],
            link=self['link'],
            price=self['price'],
            address=self['address'],
            sqft_m2=self['sqft_m2'],
            rooms=self['rooms'],
            discount=self['discount'],
            floor_elevator=self['floor_elevator']
        )
