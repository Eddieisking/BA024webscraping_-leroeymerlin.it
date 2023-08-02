"""
Project: Web scraping for customer reviews
Author: Hào Cui
Date: 06/19/2023
"""

import scrapy
from scrapy import Request
import re
from webscrapy.items import WebscrapyItem


class SpiderSpider(scrapy.Spider):
    name = "spider"
    allowed_domains = ["leroymerlin.it"]

    def start_requests(self):
        # keywords = ['dewalt', 'Stanley', 'Black+Decker', 'Craftsman', 'Porter-Cable', 'Bostitch', 'Facom', 'Proto', 'MAC Tools', 'Vidmar', 'Lista', 'Irwin', 'Lenox', 'CribMaster', 'Powers Fasteners', 'cub-cadet', 'hustler', 'troy-bilt', 'BigDog Mower',]
        exist_keywords = ['dewalt', 'stanley', 'black-decker']
        # company = 'Stanley Black and Decker'

        # from search words to generate product_urls
        for keyword in exist_keywords:
            push_key = {'keyword': keyword}
            start_urls = f'https://www.leroymerlin.it/marchi/{keyword}/?src=brd&query={keyword}'

            yield Request(
                url=start_urls,
                callback=self.parse,
                cb_kwargs={**push_key},
            )

    def parse(self, response, **kwargs):
        # Extract the pages of product_urls
        page = response.xpath(
            '//*[@id="component-productfamilypage"]//div[@class="mc-pagination__field"]/select/option[1]/text()')[
            0].extract()
        pages = [int(num) for num in page.split() if num.isdigit()][-1]

        # Based on pages to build product_urls
        keyword = kwargs['keyword']
        product_urls = [f'https://www.leroymerlin.it/marchi/{keyword}/?p={page}' for page
                        in range(1, pages + 1)]

        for product_url in product_urls:
            yield Request(url=product_url, callback=self.product_parse, meta={'product_brand': keyword})

    def product_parse(self, response: Request, **kwargs):
        product_brand = response.meta['product_brand']
        product_list = response.xpath('//*[@id="component-productfamilypage"]//ul[@class="l-resultsList '
                                      'col-container-inner js-list-products"]/li')
        for product in product_list:
            product_href = product.xpath('.//article/div[2]//a/@href')[0].extract()
            product_detailed_url = f'https://www.leroymerlin.it{product_href}'
            yield Request(url=product_detailed_url, callback=self.product_detailed_parse, meta={'product_brand': product_brand})

    def product_detailed_parse(self, response, **kwargs):
        product_brand = response.meta['product_brand']
        product_detail = response.xpath('//tbody//tr')
        product_model = 'N/A'
        product_type = 'N/A'

        for product in product_detail:
            attr = product.xpath('./th/text()')[0].extract()
            value = product.xpath('./td/text()')[0].extract()

            if attr == "Marca del prodotto":
                product_brand = value if value else 'N/A'
            elif attr == 'Modello di prodotto':
                product_model = value if value else 'N/A'
            elif attr == 'Tipo di prodotto':
                product_type = value if value else 'N/A'

        review_href = response.xpath('//*[@id="component-displaycomp"]//section[@class="col-container"]/div['
                                     '@class="col-12 m-review__link-dedicated-page"]/a/@href').extract()

        if review_href:
            review_url = f'https://www.leroymerlin.it{review_href[0]}'
            yield Request(url=review_url, callback=self.review_multiple_parse, meta={'product_brand': product_brand, 'product_model':product_model, 'product_type':product_type})

        else:
            yield Request(url=response.url, callback=self.review_single_parse, meta={'product_brand': product_brand, 'product_model':product_model, 'product_type':product_type}, dont_filter=True)

    def review_multiple_parse(self, response, **kwargs):
        product_brand = response.meta['product_brand']
        product_model = response.meta['product_model']
        product_type = response.meta['product_type']

        page_str = response.xpath('//*[@id="component-reviewdisplay"]//section[@class="col-container"]//div['
                                  '@class="mc-pagination__field"]/select/option[@value="1"]/text()')[0].extract()
        page_number = [int(num) for num in page_str.split() if num.isdigit()][-1]

        review_single_href = response.xpath('//*[@id="component-reviewdisplay"]//section['
                                            '@class="col-container"]/div/nav/a[@title="Pagina '
                                            'successiva"]/@href').extract()
        review_single_url = f'https://www.leroymerlin.it{review_single_href[0]}'

        for i in range(1, page_number + 1):
            review_single_detailed_url = re.sub(r'\?p=(\d+)', f'&page={i}#component-reviewdisplay', review_single_url)

            yield Request(url=review_single_detailed_url, callback=self.review_single_parse, meta={'product_brand': product_brand, 'product_model':product_model, 'product_type':product_type})

    def review_single_parse(self, response: Request, **kwargs):
        product_brand = response.meta['product_brand']
        product_model = response.meta['product_model']
        product_type = response.meta['product_type']
        review_list = response.xpath('//section[@class="col-container"]/div[@class="review-data kl-hidden"]')

        for review in review_list:
            item = WebscrapyItem()
            item['product_name'] = response.xpath('//div[@id="component-reviewdisplay"]/section[@class="col-container '
                                                  'l-review-container m-review-resume m-review-resume--desktop '
                                                  'js-review-resume-container"]//div['
                                                  '@class="m-review-resume__designation"]/p['
                                                  '@class="m-review-resume__designation-title"]/text()').extract_first() \
                                   or response.xpath('//*[@id="product-name"]/text()').extract_first()
            item['product_website'] = 'leroeymerlin_it'
            item['product_type'] = product_type
            item['product_brand'] = product_brand
            item['product_model'] = product_model
            item['review_id'] = review.xpath('./@data-review-id')[0].extract() or 'N/A'
            item['customer_rating'] = review.xpath('./div[@class="data-review-rating"]/text()')[0].extract() or 'N/A'
            item['customer_date'] = review.xpath('./div[@class="data-review-date"]/text()')[0].extract() or 'N/A'
            item['customer_support'] = review.xpath('./div[@class="data-review-useful"]/text()')[0].extract() or 'N/A'
            item['customer_disagree'] = review.xpath('./div[@class="data-review-not-useful"]/text()')[0].extract() or 'N/A'
            try:
                item['customer_name'] = review.xpath('./div[@class="data-review-nickname"]/text()')[0].extract()
            except IndexError as e:
                item['customer_name'] = 'N/A'
            try:
                item['customer_review'] = review.xpath('./div[@class="data-review-text"]/text()')[0].extract()
            except IndexError as e:
                item['customer_review'] = 'N/A'

            yield item
