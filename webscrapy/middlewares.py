# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals, Request
import random
from webscrapy.settings import USER_AGENT_LIST
from scrapy.exceptions import IgnoreRequest, NotConfigured

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


def get_cookies_dict():
    cookies_str = 'cookiesMigrated=1; _pcid=%7B%22browserId%22%3A%22lj1im99t2nml49kx%22%2C%22_t%22%3A%22lypxjqm0%7Clj1im9a0%22%7D; _pctx=%7Bu%7DN4IgrgzgpgThIC4B2YA2qA05owMoBcBDfSREQpAeyRCwgEt8oBJAE0RXSwH18zUAngAcAHgCsAjgFsAjAB9UYmfSkBOQjJABfIA; OptanonAlertBoxClosed=2023-06-18T14:20:54.315Z; pa_privacy=%22optin%22; _scid=da4dbe1b-4420-4763-bfe0-5e51746de001; _cs_c=1; vlz_uid=KDiCJSi1hYVZyed7I8W88hgx7EWHWfFv; _adv_ses.lmf9ehdpz.dff7=d26ddfff80354706; _gcl_au=1.1.350053527.1687098056; mics_vid=38415970260; mics_lts=1687098056780; ab_cat=A-D; ab_header=newheader; search_ab_version=1; _pin_unauth=dWlkPU5EWXpOVFF3WmpZdE1EQmtPQzAwTnpNNUxXSTVZak10WWpZeVpUaGlPVEU1TURZdw; optimizelyEndUserId=oeu1687098142582r0.1461759418183104; _vzbl_uid=H0qSHtIcXRjGUScUHb25U; iadvize-5601-consent=true; iadvize-5601-vuid=525dc25341acd9583c2e2d49ac9e2391648f135c0116c; lm-csrf=Abfa2+DFR/sZM8bC6d1T90LREJ64mXNtc2VdZkc9zm8=.1687099466217.lyWs6FHMOXymwWy1GzgVOVIg7u9kLHbDyZ21JY2VEEA=; OptanonConsent=isGpcEnabled=0&datestamp=Sun+Jun+18+2023+15%3A45%3A13+GMT%2B0100+(%E8%8B%B1%E5%9B%BD%E5%A4%8F%E4%BB%A4%E6%97%B6%E9%97%B4)&version=202303.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&genVendors=&consentId=153d4df6-abad-4a30-9599-ec2f0ed74045&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&geolocation=GB%3BENG&AwaitingReconsent=false; _cs_id=d26424c0-982a-a7d5-c92d-4486968c99db.1687098055.2.1687099513.1687098202.1618220803.1721262055101; _cs_s=16.5.0.1687101313366; _uetsid=56314b000de311ee9a289b052811f268; _uetvid=56320f700de311eea3c8c33190c1e7b1; _scid_r=da4dbe1b-4420-4763-bfe0-5e51746de001; _adv_id.lmf9ehdpz.dff7=0083a7111ae54d55.1687098055.1.1687099514.1687098055.; datadome=0L98brMze3r9erulg16hVc8QDYxx3MhbKLTItf1fa6X9QbOpHO0qAwdz_I4tLF2S5RT~ljVYfliGa52JvJzG3~82m_N4r50i2a~nZrJstNuki5fT3~_cNdrAVrzkHmzx; _dd_s=rum=0&expire=1687100416756'

    cookies_dict = {}
    for item in cookies_str.split('; '):
        key, value = item.split('=', maxsplit=1)
        cookies_dict[key] = value
    return cookies_dict


COOKIES = get_cookies_dict()


class WebscrapySpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class WebscrapyDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request: Request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        # request.cookies = COOKIES
        # request.meta = {'proxy': 'socks5://127.0.0.1:10808'}
        ua = random.choice(USER_AGENT_LIST)
        request.headers['User-Agent'] = ua
        # request.meta['proxy'] = "http://storm-stst123_area-IT:123123@eu.stormip.cn:1000"

        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


# class RotateProxyMiddleware:
#     def __init__(self, proxies_file):
#         self.proxies_file = proxies_file
#         self.proxies = self.load_proxies()
#         self.current_proxy = None
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         proxies_file = crawler.settings.get('PROXIES_FILE')
#         return cls(proxies_file)
#
#     def load_proxies(self):
#         with open(self.proxies_file, 'r') as file:
#             proxies = file.read().splitlines()
#         return proxies
#
#     def process_request(self, request, spider):
#         if not self.current_proxy:
#             self.current_proxy = self.get_random_proxy()
#
#         request.meta['proxy'] = self.current_proxy
#         print('current_proxy')
#         print(self.current_proxy)
#
#     def process_response(self, request, response, spider):
#         if response.status == 403:
#             self.remove_current_proxy()
#             self.current_proxy = self.get_random_proxy()
#             new_request = request.copy()
#             new_request.dont_filter = True  # Disable duplicate request filtering
#             return new_request
#         return response
#
#     def process_exception(self, request, exception, spider):
#         if isinstance(exception, IgnoreRequest):
#             # Handle IgnoreRequest exceptions
#             if getattr(exception, 'response', None) is not None:
#                 return self.process_response(request, exception.response, spider)
#             else:
#                 # IgnoreRequest without a response, re-raise the exception
#                 raise exception
#         elif isinstance(exception, NotConfigured):
#             # NotConfigured exception, re-raise it
#             raise exception
#         else:
#             # Handle other exceptions
#             self.remove_current_proxy()
#             self.current_proxy = self.get_random_proxy()
#             new_request = request.copy()
#             new_request.dont_filter = True  # Disable duplicate request filtering
#             return new_request
#
#     def get_random_proxy(self):
#         if not self.proxies:
#             self.proxies = self.load_proxies()  # Reload proxies from the file if the list is empty
#         return random.choice(self.proxies)
#
#     def remove_current_proxy(self):
#         if self.current_proxy in self.proxies:
#             self.proxies.remove(self.current_proxy)

"""In the following code, just need to change self.current_proxy to use new proxy"""
class RotateProxyMiddleware:
    def __init__(self):
        self.current_proxy = "http://storm-stst123_area-IT:123123@proxy.stormip.cn:1000"
        self.max_retries = 3

    @classmethod
    def from_crawler(cls, crawler):
        return cls()

    def process_request(self, request, spider):
        request.meta['proxy'] = self.current_proxy
        print('current_proxy')
        print(self.current_proxy)

    def process_response(self, request, response, spider):
        if response.status == 403:
            retries = request.meta.get('retry_times', 0)
            if retries < 3:
                new_request = request.copy()
                new_request.dont_filter = True  # Disable duplicate request filtering
                new_request.meta['retry_times'] = retries + 1
                return new_request
            else:
                self.save_unable_to_access(request.url)
        return response

    def process_exception(self, request, exception, spider):
        if isinstance(exception, IgnoreRequest):
            # Handle IgnoreRequest exceptions
            if getattr(exception, 'response', None) is not None:
                return self.process_response(request, exception.response, spider)
            else:
                # IgnoreRequest without a response, re-raise the exception
                raise exception
        elif isinstance(exception, NotConfigured):
            # NotConfigured exception, re-raise it
            raise exception
        else:
            # Handle other exceptions
            retries = request.meta.get('retry_times', 0)
            if retries < self.max_retries:
                new_request = request.copy()
                new_request.dont_filter = True  # Disable duplicate request filtering
                new_request.meta['retry_times'] = retries + 1
                return new_request
            else:
                self.save_unable_to_access(request.url)

    def save_unable_to_access(self, url):
        with open("unable to access.txt", "a") as file:
            file.write(f"Unable to access: {url}\n")

