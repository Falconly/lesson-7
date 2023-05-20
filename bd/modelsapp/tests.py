from django.test import TestCase, Client
from django.urls import reverse

from modelsapp import factories, models


# Create your tests here.
class ModelsappTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.provider = factories.Provider()
        self.product = factories.Product(provider=self.provider)
        self.product2 = factories.Product(provider=self.provider)
        self.buyer = factories.Buyer.create(products=(self.product, self.product2))
        self.buyer2 = factories.Buyer.create(products=(self.product,))

    def test_index(self):
        response = self.client.get(reverse('modelsapp:home'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'modelsapp/index.html')

    def test_list_products(self):
        response = self.client.get(reverse('modelsapp:list_products'), data={'products': self.product})

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'modelsapp/list_products.html')
        self.assertEqual(self.product.provider.company, self.provider.company)

    def test_product_detail_view(self):
        response = self.client.get(reverse('modelsapp:product', kwargs={'pk': self.product.pk}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'modelsapp/detail_product.html')
        response_detail = response.context['product']
        self.assertEqual(self.product, response_detail)

    def test_delete_product_view(self):
        pk_product = self.buyer.products.first().pk
        delete_product = self.buyer.products.first()
        response = self.client.post(reverse('modelsapp:delete_product', kwargs={'buyer_pk': self.buyer.pk,
                                                                                'pk': pk_product}), follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('modelsapp/delete_product_buyer.html')
        self.assertNotIn(delete_product, response.context['products'], 'продукт не удалился')

    def test_add_product_view(self):
        provider = factories.Provider()
        product = factories.Product.build(name="Овсянка", provider=provider)

        form_data = {'name': product.name,
                     'expiration_date': product.expiration_date,
                     'provider': product.provider.pk,
                     'price': product.price}

        response = self.client.post(reverse('modelsapp:add_product'), data=form_data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('modelsapp/add_product.html')
        self.assertEqual(product.name, models.Product.objects.last().name, 'продукт не добавлен')
        self.assertRedirects(response, reverse('modelsapp:list_products'))

    def test_update_product_view(self):
        form_data = {'name': 'Гречневая крупа',
                     'expiration_date': '',
                     'provider': self.provider.pk,
                     'price': 123.98}
        pk_product = self.product.pk

        response = self.client.post(reverse('modelsapp:update_product', kwargs={'pk': pk_product}), data=form_data,
                                    follow=True)

        pr = response.context.get('product')
        update_product = models.Product.objects.get(pk=pk_product)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('modelsapp/update_product.html')

        self.assertListEqual([pr.name, pr.expiration_date, pr.provider,  pr.price],
                             [update_product.name, update_product.expiration_date,
                              update_product.provider, update_product.price])
        self.assertRedirects(response, reverse('modelsapp:product', kwargs={'pk': pk_product}))

    def test_add_buyer_view(self):
        buyer = factories.Buyer.build(name="Юра")
        form_data = {'name': buyer.name,
                     'products': self.product.pk}

        response = self.client.post(reverse('modelsapp:add_buyer'), data=form_data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('modelsapp/add_buyer.html')
        self.assertEqual(buyer.name, models.Buyer.objects.last().name)
        self.assertRedirects(response, reverse('modelsapp:list_buyers'))
