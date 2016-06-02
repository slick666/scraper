# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class VideoField(scrapy.item.Field):
    url = scrapy.Field()
    length = scrapy.Field()
    video_type = scrapy.Field()


class VideodataItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    category = scrapy.Field()
    slug = scrapy.Field()
    title = scrapy.Field()
    summary = scrapy.Field()
    description = scrapy.Field()
    quality_notes = scrapy.Field()
    language = scrapy.Field()
    copyright_text = scrapy.Field()
    thumbnail_url = scrapy.Field()
    duration = scrapy.Field()
    videos = VideoField()
    source_url = scrapy.Field()
    tags = scrapy.Field()
    speakers = scrapy.Field()
    recorded = scrapy.Field()
