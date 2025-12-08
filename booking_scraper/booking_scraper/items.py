# booking_scraper/items.py

import scrapy

class BookingHotelItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    score = scrapy.Field()
    description = scrapy.Field()
    city = scrapy.Field()
