import factory
from faker import Factory, Faker
from .models import *

factory_ru = Factory.create('ru-Ru')
faker = Faker('ru-RU')


class Provider(factory.django.DjangoModelFactory):
    company = factory.Sequence(lambda n: 'Поставщик%s' % n)
    transport = factory_ru.word()  # ext_word_list=['Грузовой', 'Железнодорожный', 'Воздушный', 'Водный']

    class Meta:
        model = Provider


class Product(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: 'Продукт%s' % n)
    expiration_date = factory_ru.date()
    provider = factory.SubFactory(Provider)
    price = factory_ru.random_int(min=1)

    class Meta:
        model = Product


class Buyer(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: 'Миша%s' % n)

    # Реализация связи ManyToMany
    @factory.post_generation
    def products(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for product in extracted:
                self.products.add(product)

    class Meta:
        model = Buyer
