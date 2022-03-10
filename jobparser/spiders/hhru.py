import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = [
        'https://spb.hh.ru/search/vacancy?text=Python&professional_role=10&area=2&salary=&currency_code=RUR&experience=doesNotMatter&order_by=relevance&search_period=0&items_on_page=20&no_magic=true&L_save_area=true',
        # 'https://spb.hh.ru/search/vacancy?area=1&search_field=name&search_field=company_name&search_field=description&text=python&order_by=relevance&search_period=0&items_on_page=20&no_magic=true&L_save_area=true',
        # 'https://spb.hh.ru/search/vacancy?text=python&area=2&salary=&currency_code=RUR&experience=doesNotMatter&order_by=relevance&search_period=0&items_on_page=20&no_magic=true&L_save_area=true',
    ]

    # custom_settings = {}  # персональные настройки для каждого паука

    def parse(self, response: HtmlResponse):  # (вызывается метод в отдельном потоке для каждой точки входа (start_urls) - ограничивается аппаратными характеристиками машины).
                    # response: HtmlResponse  # - указываем, что response является объектом класса HtmlResponse
        # response.css()  # возможно собирать по css селекторам

        next_page = response.xpath("//a[@data-qa='pager-next']/@href").get()  # аналогчно getall, только для ПЕРВОГО эл-та списка
        if next_page:
            yield response.follow(next_page, callback=self.parse)  # yield для перехода на новую страницу, рекурсивный вызов self.parse в кач-ве callback-функции

        links = response.xpath("//a[@data-qa='vacancy-serp__vacancy-title']/@href").getall()  # без getall будет возвращаться ОБЪЕКТЫ
        for link in links:
            print('====================================== next link: ====================================== \n',
                  link, )
            print()
            yield response.follow(link, callback=self.vacancy_parse)  # parse делаем асинхронным (для сокращ.времени ожидания)
                        # т.о. цикл for не будет ждать окончания работы тела цикла (response.follow) и пойдет сразу дальше

    def vacancy_parse(self, response: HtmlResponse):
        name = response.xpath("//h1/text()").get()
        salary = response.xpath("//div[@data-qa='vacancy-salary']/span/text()").getall()
        url = response.url  # не парсим ссылку с сайта, тк url есть в response

        yield JobparserItem(name=name, salary=salary, url=url)  # разработчики scrapy рекомендуют именно yield
                                                                # (предположительно для более оптимального использования памяти)

