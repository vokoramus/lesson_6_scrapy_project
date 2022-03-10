# создали вручную данный файл для возможности отладки логики работы паука

from scrapy.crawler import CrawlerProcess  # основной класс
from scrapy.settings import Settings  # глобальный класс настроек

from jobparser import settings
from jobparser.spiders.hhru import HhruSpider
from jobparser.spiders.sjru import SjruSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)  # файл settings.py будет распарсен и передан сюда в виде объекта, похожего на словарь

    process = CrawlerProcess(settings=crawler_settings)  # обязательно нужно передать настройки
    # process.crawl(HhruSpider)  # в процесс сажаем паука
    process.crawl(SjruSpider)  # в процесс сажаем паука
    process.start()
