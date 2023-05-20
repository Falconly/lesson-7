from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import *
from .models import *


# Create your views here.
def index_view(request):
    context = {'title': 'Главная страница'}
    return render(request, 'modelsapp/index.html', context=context)


class ListProducts(ListView):
    model = Product
    template_name = 'modelsapp/list_products.html'
    context_object_name = 'products'
    extra_context = {'title': 'Список продуктов',
                     'form': ProductSearchNameForm,
                     'form_price': ProductSearchPriceForm}

    ordering = ('-id',)

    def get_queryset(self):
        qs = Product.objects.all()

        product_name = self.request.GET.get('product_name')
        product_price = self.request.GET.get('product_price')

        if product_name or product_price:
            qs = qs.filter(Q(name=product_name) | Q(price=product_price))
        ordering = self.get_ordering()
        qs = qs.order_by(*ordering)
        return qs


class ProductViews(DetailView):
    model = Product
    template_name = 'modelsapp/detail_product.html'
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = get_object_or_404(Product, pk=self.kwargs['pk'])
        c_def = {'title': f'Продукт - {product.name}'}
        context.update(c_def)
        return context


def list_buyer_view(request):
    buyers = Buyer.objects.all()
    context = {'title': 'Список покупателей', 'buyers': buyers}
    return render(request, 'modelsapp/list_buyers.html', context=context)


def detail_buyer_view(request, buyer_pk):
    buyer = get_object_or_404(Buyer, pk=buyer_pk)
    products = buyer.products.all()
    context = {'title': f'Покупатель - {buyer.name}',
               'buyer': buyer,
               'products': products,
               }
    return render(request, 'modelsapp/detail_buyer.html', context=context)


def delete_product_view(request, buyer_pk, pk):
    buyer = Buyer.objects.get(pk=buyer_pk)
    product = Product.objects.get(pk=pk)
    buyer.products.remove(product)  # Удаление отношения между моделями Buyer, Product
    buyer.save()
    return redirect('modelsapp:buyer', buyer_pk=buyer_pk)


class AddProductView(CreateView):
    form_class = AddProductForm
    template_name = 'modelsapp/add_product.html'
    extra_context = {'title': 'Добавление продукта',
                     'button_name': 'Добавить'}
    success_url = reverse_lazy('modelsapp:list_products')
    model = Product


class UpdateProductView(UpdateView):
    model = Product
    form_class = AddProductForm
    template_name = 'modelsapp/add_product.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = get_object_or_404(Product, pk=self.kwargs['pk'])
        c_def = {'title': f'Редактирование продукта - {product.name}',
                 'button_name': 'Редактировать'}
        context.update(c_def)
        return context

    def get_object(self, queryset=None):
        slug = self.kwargs.get('pk')
        product = get_object_or_404(Product, pk=slug)
        return product


class DeleteProductView(DeleteView):
    model = Product
    template_name = 'modelsapp/delete_product_buyer.html'
    success_url = reverse_lazy('modelsapp:list_products')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = get_object_or_404(Product, pk=self.kwargs['pk'])
        c_def = {'title': f'Удаление продукта - {product.name}'}
        context.update(c_def)
        return context


def get_object(self, queryset=None):
    slug = self.kwargs.get('pk')
    product = get_object_or_404(Product, pk=slug)
    return product


class AddBuyerView(CreateView):
    model = Buyer
    form_class = AddBuyerForm
    template_name = 'modelsapp/add_buyer.html'
    success_url = reverse_lazy('modelsapp:list_buyers')
    extra_context = {'title': 'Добавление покупателя',
                     'button_name': 'Добавить'}


class UpdateBuyerView(UpdateView):
    model = Buyer
    form_class = AddBuyerForm
    template_name = 'modelsapp/add_buyer.html'
    success_url = reverse_lazy('modelsapp:list_buyers')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        buyer = get_object_or_404(Buyer, pk=self.kwargs['buyer_pk'])
        c_def = {'title': f'Редактирование покупателя - {buyer.name}',
                 'button_name': 'Редактировать'}
        context.update(c_def)
        return context

    def get_object(self, queryset=None):
        slug = self.kwargs.get('buyer_pk')
        buyer = get_object_or_404(Buyer, pk=slug)
        return buyer


class DeleteBuyerView(DeleteView):
    model = Buyer
    template_name = 'modelsapp/delete_product_buyer.html'
    success_url = reverse_lazy('modelsapp:list_buyers')
    extra_context = {'title': 'Удаление покупателя'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        buyer = get_object_or_404(Buyer, pk=self.kwargs['buyer_pk'])
        c_def = {'title': f'Удаление покупателя - {buyer.name}'}
        context.update(c_def)
        return context

    def get_object(self, queryset=None):
        slug = self.kwargs.get('buyer_pk')
        buyer = get_object_or_404(Buyer, pk=slug)
        return buyer
