import scrapy


class CortlandScrapper(scrapy.Spider):
    name = 'cortland'

    start_urls = [
        'https://www.cortland.pl/apple-iphone/wszystkie.html',
        'https://www.cortland.pl/komputery-mac/macbook-air.html',
        'https://www.cortland.pl/komputery-mac/macbook-pro.html',

    ]

    custom_settings = {
        'COLLECTION_NAME': 'products'
    }

    def parse(self, response):
        for products in response.css('div.ty-compact-list__item'):
            yield {
                'name': products.css('a.product-title::text').get(),
                'old_price': products.css('span.ty-list-price::text').get(),
                'actual_price': products.css('span.ty-price span.ty-price-num::text').extract()[1:2],
                'link': products.css('a.product-title').attrib['href'],
                'image':products.css('img.ty-pict').attrib['src'],
                'shop': 'Cortland',
                'category':self.GetCategoryByProductName(products.css('a.product-title::text').get())
            }
        next_page = response.css('a.ty-pagination__next::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def GetCategoryByProductName(self, value: str) -> str:
        if "iphone" in value.lower():
            return "Phone"
        elif "mac" in value.lower():
            return "Laptop"
        elif "ipad" in value.lower():
            return "Tablet"
        else:
            return "Other"



