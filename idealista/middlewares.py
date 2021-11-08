from scrapy.http import HtmlResponse
from selenium import webdriver


class JSMiddleware(object):
    def process_request(self, request, spider):
        driver = webdriver.Firefox()
        driver.get(request.url)

        body = driver.page_source
        return HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=request)