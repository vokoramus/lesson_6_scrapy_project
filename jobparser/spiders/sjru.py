import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://spb.superjob.ru/vacancy/search/?keywords=Python',
                  ]

    def parse(self, response: HtmlResponse):  # (вызывается метод в отдельном потоке для каждой точки входа (start_urls) - ограничивается аппаратными характеристиками машины).
                    # response: HtmlResponse  # - указываем, что response является объектом класса HtmlResponse
        # response.css()  # возможно собирать по css селекторам

        next_page_xpath = "//a[contains(@class, 'button-dalshe')]/@href"
        next_page = response.xpath(next_page_xpath).get()  # аналогчно getall, только для ПЕРВОГО эл-та списка
        if next_page:
            yield response.follow(next_page, callback=self.parse)  # yield для перехода на новую страницу, рекурсивный вызов self.parse в кач-ве callback-функции

        # //div[@class='f-test-search-result-item']                                         # 7шт мусора из 27
        # //div[@class='f-test-search-result-item']//span[contains(@class, 'salary')]       # ровно 20 результатов
        links_xpath = "//div[@class='f-test-search-result-item']//span[contains(@class, 'salary')]/../span/a/@href"
        links = response.xpath(links_xpath).getall()  # без getall будет возвращаться ОБЪЕКТЫ
        for link in links:
            print('current link:', link)
            print()
            yield response.follow(link, callback=self.vacancy_parse)  # parse делаем асинхронным (для сокращ.времени ожидания)
                        # т.о. цикл for не будет ждать окончания работы тела цикла (response.follow) и пойдет сразу дальше



    def vacancy_parse(self, response: HtmlResponse):
        name_xpath = "//div[contains(@class, 'vacancy-base-info')]//h1/text()"

        # //div[contains(@class, 'vacancy-base-info')]//h1/following-sibling::span/span[1]
        # //div[contains(@class, 'vacancy-base-info')]//h1/following-sibling::span/span[2]
        salary_xpath = "//div[contains(@class, 'vacancy-base-info')]//h1/following-sibling::span/span[1]/text()"
        period_xpath = "//div[contains(@class, 'vacancy-base-info')]//h1/following-sibling::span/span[2]/text()"

        name = response.xpath(name_xpath).get()
        salary = response.xpath(salary_xpath).getall()
        period = response.xpath(period_xpath).get()
        url = response.url  # не парсим ссылку с сайта, тк url есть в response

        yield JobparserItem(name=name, salary=salary, period=period, url=url)  # разработчики scrapy рекомендуют именно yield
                                                                # (предположительно для более оптимального использования памяти)

