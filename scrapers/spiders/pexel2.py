# -*- coding: utf-8 -*-
import scrapy


class Pexel2Spider(scrapy.Spider):
    name = 'pexel2'
    allowed_domains = ['https://www.pexels.com/']
    start_urls = [
        'https://www.pexels.com/?format=html&page=1',
        'https://www.pexels.com/?format=html&page=2',
        'https://www.pexels.com/?format=html&page=3',
        'https://www.pexels.com/?format=html&page=4',
        'https://www.pexels.com/?format=html&page=5',
        'https://www.pexels.com/?format=html&page=6',
        'https://www.pexels.com/?format=html&page=7',
        'https://www.pexels.com/?format=html&page=8',
        'https://www.pexels.com/?format=html&page=9',
        'https://www.pexels.com/?format=html&page=10',
    ]

    """
    <img srcset="https://images.pexels.com/photos/1959128/pexels-photo-1959128.jpeg?auto=compress&amp;cs=tinysrgb&amp;dpr=1&amp;w=500 1x, https://images.pexels.com/photos/1959128/pexels-photo-1959128.jpeg?auto=compress&amp;cs=tinysrgb&amp;dpr=2&amp;w=500 2x"
     class="photo-item__img" 
     alt="Man Holding Red Rose" 
     data-image-width="3437"
     data-image-height="5030"
     data-big-src="https://images.pexels.com/photos/1959128/pexels-photo-1959128.jpeg?auto=compress&amp;cs=tinysrgb&amp;h=750&amp;w=1260" 
     data-large-src="https://images.pexels.com/photos/1959128/pexels-photo-1959128.jpeg?auto=compress&amp;cs=tinysrgb&amp;h=650&amp;w=940" 
     data-tiny-src="https://images.pexels.com/photos/1959128/pexels-photo-1959128.jpeg?auto=compress&amp;cs=tinysrgb&amp;dpr=1&amp;w=500" 
     data-tiny-srcset="https://images.pexels.com/photos/1959128/pexels-photo-1959128.jpeg?auto=compress&amp;cs=tinysrgb&amp;dpr=1&amp;w=500 1x, https://images.pexels.com/photos/1959128/pexels-photo-1959128.jpeg?auto=compress&amp;cs=tinysrgb&amp;dpr=2&amp;w=500 2x" 
     data-pin-media="https://images.pexels.com/photos/1959128/pexels-photo-1959128.jpeg?auto=compress&amp;cs=tinysrgb&amp;fit=crop&amp;h=1200&amp;w=800" 
     src="https://images.pexels.com/photos/1959128/pexels-photo-1959128.jpeg?auto=compress&amp;cs=tinysrgb&amp;dpr=1&amp;w=500">
    """

    def parse(self, response):
        images = response.css('img.photo-item__img')
        for image in images:
            print(image.extract())
            yield {
                'title':image.css('img::attr(alt)').extract_first(),
                'src':image.css('img::attr(src)').extract_first(),
            }
