"""
# Project: proxies pool
# Author: Eddie
# Date: 18/06/2023
"""

# Clear the proxy_text
import requests

proxy_text = 'proxy_text.txt'

with open(proxy_text, 'w') as file:
    file.write('')


def proxy_generation(number):
    for i in range(number):
        ###########
        proxyip = "https://storm-stst123_area-IT:123123@eu.stormip.cn:1000"
        url = "http://myip.ipip.net"
        proxies = {
            'http': proxyip,
            'https': proxyip,
        }
        with open(proxy_text, 'a') as file:
            file.write(proxyip)
            file.write('\n')

        print("Data saved to", proxy_text)

# Change the number to decide the number of proxies generated
# proxy_generation(20)


# """Another way to get proxy"""
# import requests
#
# # Clear the proxy_text
# proxy_text = 'proxy_text.txt'
# with open(proxy_text, 'w') as file:
#     file.write('')
#
# url = 'https://api.stormproxies.cn/web_v1/ip/get-ip-v3?app_key=64318690cd8b0c33d643b078d3974ebf&pt=9&num=20&ep=&cc=IT&state=&city=&life=30&protocol=1&format=txt&lb=%5Cr%5Cn'
# response = requests.get(url)
# proxies = response.text.split('\n')
#
# with open(proxy_text, 'a') as file:
#     for proxy in proxies:
#         file.write('http://' + proxy + '\n')
#
# print("Data saved to", proxy_text)


