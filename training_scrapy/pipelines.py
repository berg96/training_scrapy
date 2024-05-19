# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from sqlalchemy import Column, Integer, String, Text, create_engine
from sqlalchemy.orm import declarative_base, Session

Base = declarative_base()


class Quote(Base):
    __tablename__ = 'Quote'  # Задали имя таблицы в БД.
    id = Column(Integer, primary_key=True)
    text = Column(Text)
    author = Column(String(200))
    tags = Column(String(400))


class QuotesToDBPipeline:

    def open_spider(self, spider):
        # Создание "движка" алхимии.
        engine = create_engine('sqlite:///sqlite.db')
        # Создание всех таблиц.
        Base.metadata.create_all(engine)
        # Создание сессии как атрибута объекта.
        self.session = Session(engine)

    def process_item(self, item, spider):
        # Создание объекта цитаты.
        quote = Quote(
            text=item['text'],
            author=item['author'],
            tags=', '.join(item['tags']),
        )
        # Добавление объекта в сессию и коммит сессии.
        self.session.add(quote)
        self.session.commit()
        # Возвращаем item, чтобы обработка данных не прерывалась.
        return item

    def close_spider(self, spider):
        self.session.close()
