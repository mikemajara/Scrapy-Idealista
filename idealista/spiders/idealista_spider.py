__author__ = 'David Carrasco'
import scrapy
from idealista.items import IdealistaItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from datetime import datetime
from scrapy_selenium import SeleniumRequest

class IdealistaSpider(CrawlSpider):
    name = "idealista"
    allowed_domains = ["idealista.com"]
    ########################################################################
    ###       Add the url to crawl in the start_urls variable           ###
    ########################################################################
    #start_urls = ["https://www.idealista.com/venta-viviendas/leganes/el-carrascal/"]
    #start_urls = ['https://www.idealista.com/alquiler-viviendas/madrid/zona-norte/']

    header = {'Host': 'https://www.idealista.com/',
              'User-Agent': 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; http://www.google.com/bot.html) Chrome/W.X.Y.Z‡ Safari/537.36',
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
              'Accept-Language': 'en-US,en;q=0.8,es-ES;q=0.5,es;q=0.3',
              'Connection': 'keep-alive',
              'Referer': 'https://www.idealista.com/',
              'Upgrade-Insecure-Requests': '1',
              'Sec-Fetch-Dest': 'document',
              'Sec-Fetch-Mode': 'navigate',
              'Sec-Fetch-Site': 'same-origin',
              'Sec-Fetch-User': '?1',
              'Sec-GPC': '1'
              }

    start_urls = ['https://www.idealista.com/venta-viviendas/murcia-murcia/']

    def start_requests(self):
        for url in self.start_urls:
            # yield scrapy.Request(url=url, callback=self.parse_flats
            # , headers=self.header
            # )
            yield SeleniumRequest(url=url,callback=self.parse_flats)

    # rules = (
    #         # Filter all the flats paginated by the website following the pattern indicated
    #         Rule(LinkExtractor(restrict_xpaths=("//a[@class='icon-arrow-right-after']")),
    #              callback='parse_flats',
    #              follow=True),
    #     )

    def parse_flats(self, response):

    	# Necessary in order to create the whole link towards the website
        default_url = 'http://idealista.com'
        
        info_flats_xpath = response.xpath("//*[@class='item-info-container']")
        prices_flats_xpath = response.xpath("//*[@class='row price-row clearfix']/span[@class='item-price h2-simulated']/text()")
        discounts_xpath = response.xpath("//*[@class='row price-row clearfix']")

        links = [str(''.join(default_url + link.xpath('a/@href').extract().pop()))
                 for link in info_flats_xpath]

        prices = [float(flat.extract().replace('.','').strip())
                 for flat in prices_flats_xpath]
                 
        discounts = [0 if len(discount.xpath("./*[@class='item-price-down icon-pricedown']/text()").extract()) < 1
                     else discount.xpath("./*[@class='item-price-down icon-pricedown']/text()").extract().pop().replace('.','').strip().split(' ').pop(0) 
                     for discount in discounts_xpath]
        
        addresses = [address.xpath('a/@title').extract().pop().encode('iso-8859-1')
		     for address in info_flats_xpath]
                     
        rooms = [int(flat.xpath('span[@class="item-detail"]/small[contains(text(),"hab.")]/../text()').extract().pop().strip()) 
                 if len(flat.xpath('span[@class="item-detail"]/small[contains(text(),"hab.")]')) == 1 
                 else None 
                 for flat in info_flats_xpath]
                 
        sqfts_m2 = [float(flat.xpath('span[@class="item-detail"]/small[starts-with(text(),"m")]/../text()').extract().pop().replace('.','').strip())
                    if len(flat.xpath('span[@class="item-detail"]/small[starts-with(text(),"m")]')) == 1 
                    else None 
                    for flat in info_flats_xpath]
                    
        floors_elevator = [flat.xpath('string(span[@class="item-detail"][last()])').extract().pop().strip()
                           for flat in info_flats_xpath]
                           
        for flat in zip(links, prices, addresses, discounts, sqfts_m2, rooms, floors_elevator):
            item = IdealistaItem(date=datetime.now().strftime('%Y-%m-%d'),
				 link=flat[0], price=flat[1], address=flat[2], discount=flat[3], 
                                 sqft_m2=flat[4], rooms=flat[5], floor_elevator = flat[6])
            yield item.to_json()

    #Overriding parse_start_url to get the first page
    parse_start_url = parse_flats


