import scrapy


class NoonSpider(scrapy.Spider):
    name = 'noon'
    allowed_domains = ['noon.com']
    start_urls = ['https://www.noon.com/egypt-en/sports-and-outdoors/exercise-and-fitness/yoga-16328/']

    def parse(self, response):
        products = response.xpath('//div[@class="productContainer"]')
        for product in products:
            yield {
                'title': product.xpath('.//div[@class="product-title"]/text()')
                               .get(default='').strip(),
                'price': product.xpath('.//span[contains(@class, "sellingPrice")]/text()')
                               .get(default='').strip(),
                'brand': product.xpath('.//div[contains(text(), "Brand")]/following-sibling::div/text()')
                               .get(default='').strip(),
                'category': product.xpath('.//div[contains(text(), "Category")]/following-sibling::div/text()')
                                  .get(default='').strip(),
                'url': response.urljoin(product.xpath('./a/@href').get())
            }

        next_page = response.xpath('//a[contains(text(), "Next")]/@href').get()
        if next_page:
            yield response.follow(next_page, self.parse)
