from scraper.spiders import spare_parts_spider
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess

process = CrawlerProcess(get_project_settings())

# process.crawl(spare_parts_spider.SparePartsSpider, url='https://www.kfzteile24.de/artikeldetails?ktypnr=142450&returnTo=rm%3DshowArticles%26ktypnr%3D142450%26node%3D0%252C1%252C100004%252C100222%252C100317%252C100327%231&search=1240-130879')
process.crawl(spare_parts_spider.SparePartsSpider, categories_url='https://www.kfzteile24.de/?ktypnr=142450')


process.start()
