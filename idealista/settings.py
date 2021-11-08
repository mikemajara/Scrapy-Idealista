# -*- coding: utf-8 -*-

# Scrapy settings for idealista project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

from .proxies import get_proxies
from shutil import which

###########################
# Main configuration
###########################

BOT_NAME = 'idealista'

SPIDER_MODULES = ['idealista.spiders']
NEWSPIDER_MODULE = 'idealista.spiders'

SELENIUM_DRIVER_NAME = 'chrome'
SELENIUM_DRIVER_EXECUTABLE_PATH = '/usr/local/bin/chromedriver'
# SELENIUM_DRIVER_ARGUMENTS=['-headless']  # '--headless' if using chrome instead of firefox

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_useragents.downloadermiddlewares.useragents.UserAgentsMiddleware': 500,
    'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
    'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
    # https://stackoverflow.com/a/47319968/3157057
    # Option 1: needs to be running Splash.
    # 'scrapy_splash.SplashCookiesMiddleware': 723,
    # 'scrapy_splash.SplashMiddleware': 725,
    # Option 2
    'scrapy_selenium.SeleniumMiddleware': 800,
    # 'idealista.middlewares.JSMiddleware': 200,
}

DEFAULT_REQUEST_HEADERS = {
    'authority': 'www.idealista.com',
    'upgrade-insecure-requests': '1',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest':' document'
}

FEED_EXPORT_ENCODING='utf-8'

DOWNLOAD_TIMEOUT = 10
DOWNLOAD_DELAY = 10

CONCURRENT_REQUESTS_PER_DOMAIN = 1
CONCURRENT_REQUESTS = 1


###########################
# User agent configurarion
###########################

USER_AGENTS = [
    ('Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; http://www.google.com/bot.html) Chrome/W.X.Y.Z‡ Safari/537.36 '),
    # ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko; compatible) Chrome/81.0.4044.113 Safari/537.36'),
    # ('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0')
    
    # Add more user agents which actually work nowadays
]

#########################
# Proxies configuration
#########################

RETRY_HTTP_CODES = [500, 502, 503, 504, 400, 403, 404, 408]

ROTATING_PROXY_PAGE_RETRY_TIMES = 99999999999 # TODO: is it possible to setup this parameter with no limit?
ROTATING_PROXY_LIST = get_proxies()

ROBOTSTXT_OBEY = False
