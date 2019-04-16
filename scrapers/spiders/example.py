import scrapy
import re
from scrapy.linkextractor import LinkExtractor
from scrapy.selector import Selector


class PexelsScraper(scrapy.Spider):
    name = "pexels"
    url_matcher = re.compile('^https:\/\/www\.pexels\.com\/photo\/')
    crawled_ids = set()
    src_extractor = re.compile('src="([^"]*)"')
    tags_extractor = re.compile('alt="([^"]*)"')

    @property
    def start_requests(self):
        url = "https://www.pexels.com/"
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        body = Selector(text=response.body)
        images = body.css('img.image-section__image').extract()
        for image in images:
            img_url = PexelsScraper.src_extractor.findall(image)[0]
            tags = [tag.replace(',', '').lower()
                    for tag in PexelsScraper.tags_extractor.findall(image)[0].split(' ')]
            print(img_url, tags)
            link_extractor = LinkExtractor(allow=PexelsScraper.url_matcher)
        next_links = [link.url for link in link_extractor.extract_links(response) if not self.is_extracted(link.url)]
        for link in next_links:
            yield scrapy.Request(link, self.parse)

    def is_extracted(self, url):
        id = int(url.split('/')[-2].split('-')[-1])
        if id not in PexelsScraper.crawled_ids:
            PexelsScraper.crawled_ids.add(id)
            return False
        return True
