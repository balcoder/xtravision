#!/usr/bin/env python
# encoding=utf-8

from scrapy.spider import BaseSpider 
from scrapy.selector import HtmlXPathSelector

from xtravision.items import XtravisionItem

class XtravisionSpider(BaseSpider):
   ''' This spider will crawl the xtra-vision.com website and extract the name
      , url and price(if the movie is for sale aswell as for rent)of
      new release movies and return an item[] with these fields '''
   
   # need to define three mandatory attributes: name, allowed_domains, start_urls
   name = "xtravision"
   allowed_domains = ["xtra-vision.ie"]
   start_urls = [
       "http://www.xtra-vision.ie/dvd-blu-ray/to-rent/new-release/dvd.html/",
       "http://www.xtra-vision.ie/dvd-blu-ray/to-rent/new-release/dvd.html?p=2"]

   # parse is called with the downloaded response object of each start url
   def parse(self, response):
       hxs = HtmlXPathSelector(response)
       links = hxs.select('//a[@class="product-image"]')
       items = []
       
       # loop through each selector result and extract fields defined in items.py
       for link in links: 
           item = XtravisionItem()
           item['movie'] = link.select('h2[@class="product-name"]/text()').extract()
           item['link'] = link.select('@href').extract()
           # need to clean up price by joining integer to decimal and removing extra tabs
           price = link.select('div[@class="price-box"]//span[@class="price"]/text()').extract()
           pricebit = link.select('div[@class="price-box"]//span[@class="price"]/sub[@class="price-bit"]/text()').extract()
           price = price + pricebit
           totalprice = ''.join(price).replace('\t','')
           # need to remove the unicode for euro sign
           item['price'] = totalprice[1:] 
           items.append(item)           
       return items 
