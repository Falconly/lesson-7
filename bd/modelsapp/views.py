from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from .models import *


# Create your views here.
def index_view(request):
    context = {'title': 'Главная страница'}
    return render(request, 'modelsapp/index.html', context=context)


class ListProducts(ListView):
    model = Product
    template_name = 'modelsapp/list_products.html'
    context_object_name = 'products'
    extra_context = {'title': 'Список продуктов', 'flag': False}


class ProductViews(DetailView):
    model = Product
    template_name = 'modelsapp/list_products.html'
    context_object_name = "product"
    extra_context = {'title': f'Продукт', 'flag': True}


def list_buyer_view(request):
    buyers = Buyer.objects.all()
    context = {'title': 'Список покупателей', 'buyers': buyers, 'flag': False}
    return render(request, 'modelsapp/list_buyers.html', context=context)


def detail_buyer_view(request, buyer_pk):
    buyer = get_object_or_404(Buyer, pk=buyer_pk)
    products = buyer.products.all()
    context = {'title': f'Покупатель - {buyer.name}',
               'flag': True,
               'buyer': buyer,
               'products': products}
    return render(request, 'modelsapp/list_buyers.html', context=context)


def delete_product_view(request, buyer_pk, pk):
    buyer = Buyer.objects.get(pk=buyer_pk)
    product = Product.objects.get(pk=pk)
    buyer.products.remove(product)  # Удаление отношения между моделями Buyer, Product
    buyer.save()
    return redirect('buyer', buyer_pk=buyer_pk)
