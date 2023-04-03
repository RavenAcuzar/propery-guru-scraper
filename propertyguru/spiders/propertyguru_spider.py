from urllib.parse import urlencode
import scrapy
import requests
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.environ.get("API_KEY")

def get_scrapeops_url(url):
    payload = {'api_key': API_KEY, 'url': url}
    proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
    return proxy_url

class PropertyguruSpiderSpider(scrapy.Spider):
    name = "propertyguru_spider"
    
    def start_requests(self):
        yield scrapy.Request(get_scrapeops_url('https://www.propertyguru.com.my/property-for-sale?search=true&sort=date&order=desc'), callback=self.parse)

    def parse(self, response):
        for property_url in response.css('div.gallery-container a.nav-link::attr(href)').getall():
            yield scrapy.Request(get_scrapeops_url(property_url), callback=self.download_html)
        
        # follow pagination links
        next_page_url = f"https://www.propertyguru.com.my{response.css('li.pagination-next a::attr(href)').get()}"
        if next_page_url:
            yield scrapy.Request(get_scrapeops_url(next_page_url), callback=self.parse)
    
    def download_html(self, response):
        #download html here to save in blob
        yield response
    
    #use to scrape data from html
    # def parse_property(self, response):
        # print(response.text)
        # yield {
        #     'title': response.css('h1.h2.text-transform-none ::text').get().strip(),
        #     'address': response.css('div#map-canvas::attr(data-marker-label)').get() if response.css('div#map-canvas::attr(data-marker-label)').get() else response.css('span[itemprop="streetAddress"] ::text').get(),
        #     'longtitude':response.css('div#map-canvas::attr(data-longitude)').get(),
        #     'latitude':response.css('div#map-canvas::attr(data-latitude)').get(),
        #     'price': response.css('span.element-label.price::attr(content)').get(),
        #     'area': response.css('div[itemprop="floorSize"] span.element-label ::text').get().strip(),
        #     'bedrooms': response.css('span[itemprop="numberOfRooms"] ::text').get(),
        #     'bathrooms': response.css('div.property-info-element.baths span.element-label ::text').get(),
        #     # 'description': response.css('.listing-description-text ::text').getall(),
        #     # 'amenities': response.css('.amenities-list .amenity ::text').getall(),
        #     }
