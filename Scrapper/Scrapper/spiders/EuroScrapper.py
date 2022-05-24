import scrapy


class EuroScrapper(scrapy.Spider):
    name = 'euro'

    page = 2
    start_urls = [
        'https://www.euro.com.pl/telefony-komorkowe,_Apple.bhtml'
    ]

    custom_settings = {
        'COLLECTION_NAME': 'products'
    }

    def GetCategoryByProductName(self, value: str) -> str:
        if "iphone" in value.lower():
            return "Phone"
        elif "mac" in value.lower():
            return "Laptop"
        elif "ipad" in value.lower():
            return "Tablet"
        else:
            return "Other"

    def parse(self, response):
        for products in response.css('div.product-for-list'):
            try:
                item1 = products.css('div.attributes-row  span::text, div.attributes-row a::text').getall()
                item = [i.strip() for i in item1 if i.strip()]
                print(item)
                yield {
                    'name': products.css('h2.product-name a::text').get().strip(),
                    'price': products.css('div.price-normal::text').get().strip(),
                    'oldprice': products.css('div.price-old::text').get().strip(),
                    'category': self.GetCategoryByProductName(products.css('p.product-category a::text').get().strip()),
                    'link': "https://www.euro.com.pl" + products.css('h2.product-name a').attrib['href'],
                    'shop': 'RTVeuroAGD',
                    'img': products.css('a.photo-hover img::attr(data-original)').get(),
                    'details': {
                        item[i]: item[i + 1].strip() for i in range(0, len(item), 2)
                    }
                }
            except:
                item1 = products.css('div.attributes-row  span::text, div.attributes-row a::text').getall()
                item = [i.strip() for i in item1 if i.strip()]
                yield {
                    'name': products.css('h2.product-name a::text').get().strip(),
                    'actual_price': products.css('div.price-normal::text').get().strip(),
                    'old_price': "",
                    'category': products.css('p.product-category a::text').get().strip(),
                    'link': "https://www.euro.com.pl" + products.css('h2.product-name a').attrib['href'],
                    'shop': 'RTVeuroAGD',
                    'img': products.css('a.photo-hover img::attr(data-original)').get(),
                    'details': {
                        item[i]: item[i + 1] for i in range(0, len(item), 2)
                    }
                }

        next_page = "https://www.euro.com.pl/telefony-komorkowe,_Apple,strona-" + str(self.page) + ".bhtml"

        numbers_list = [int(x.strip()) for x in response.css("div.paging-numbers a::text").extract()]
        page_number = max(numbers_list)

        if self.page <= page_number:
            try:
                yield response.follow(next_page, callback=self.parse)
                self.page += 1
            except:
                return
        else:
            scrapy.Spider.close(self, reason="Cannot find url")
