import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BooksCrawlerSpider(CrawlSpider):
    name = "books_crawler"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["http://books.toscrape.com/"]


    link_book = LinkExtractor(restrict_css='h3>a')
    #link of the next pages
    link_next = LinkExtractor(restrict_css='.next>a')
    #link of categories
    link_cats = LinkExtractor(restrict_css='.side_categories>ul>li>ul>li>a')
    
    rule_book_details = Rule( link_book,callback="parse_item", follow=False)
    rule_next_link = Rule( link_next, follow=True)
    rule_categories = Rule( link_cats, follow=True)
    
    rules = {
        rule_book_details,
        rule_next_link,
        rule_categories    
        
    }

    def parse_item(self, response):
        yield  {
            'Title':response.css('h1::text').get(),
            'Category':response.xpath('//ul[@class="breadcrumb"]/li[last()-1]/a/text()').get(),
            'Link':response.url
            
        }
       
