from django.db import models


# Create your models here.
class Provider(models.Model):
    company = models.CharField(max_length=100, verbose_name="Название транспортной компании", unique=True)
    delivery_date = models.DateField(verbose_name="Дата поставки")
    transport = models.CharField(max_length=100, verbose_name="Тип транспорта")

    def __str__(self):
        return self.company

    class Meta:
        verbose_name = "Поставщики"
        verbose_name_plural = "Поставщики"


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название продукта", unique=True)
    expiration_date = models.DateField(default=None, verbose_name="Срок годности")
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, default=None, verbose_name="Поставщик")
    price = models.DecimalField(max_digits=100, decimal_places=2, verbose_name="Цена")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Продукты"
        verbose_name_plural = "Продукты"


class Buyer(models.Model):
    name = models.CharField(max_length=50, verbose_name="Имя покупателя")
    products = models.ManyToManyField(Product, verbose_name="Продукты")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Покупатели'
        verbose_name_plural = "Покупатели"