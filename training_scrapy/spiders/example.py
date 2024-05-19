import scrapy

from training_scrapy.items import QuoteItem


class QuotesSpider(scrapy.Spider):
    # Имя паука должно быть уникальным в рамках одного проекта.
    name = "quotes"
    # Список стартовых ссылок, с которых паук начнёт парсить данные.
    start_urls = ['http://quotes.toscrape.com/',]

    # Метод, загружающий и обрабатывающий каждую из стартовых ссылок.
    def parse(self, response):
        for quote in response.css('div.quote'):
            # Для каждой найденной цитаты создаём и возвращаем словарь:
            data = {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('a.tag::text').getall(),
            }
            # Передаём словарь с данными в конструктор класса
            yield QuoteItem(data)

            # По CSS-селектору ищем ссылку на следующую страницу.
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            # Если ссылка нашлась, загружаем страницу по ссылке
            # и вызываем метод parse() ещё раз.
            yield response.follow(next_page, callback=self.parse)
