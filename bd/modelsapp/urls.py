from django.urls import path

from .views import *

app_name = 'modelsapp'

urlpatterns = [path('list_products/', ListProducts.as_view(), name="list_products"),
               path('', index_view, name="home"),
               path('product/<int:pk>/', ProductViews.as_view(), name="product"),
               path('list_buyers/', list_buyer_view, name="list_buyers"),
               path('buyer/<int:buyer_pk>/', detail_buyer_view, name="buyer"),
               path('buyer/<int:buyer_pk>/product/<int:pk>', delete_product_view, name="delete_product"),
               path('add_product/', AddProductView.as_view(), name="add_product"),
               path('product/<int:pk>/update_product/', UpdateProductView.as_view(), name="update_product"),
               path('product/<int:pk>/delete_product', DeleteProductView.as_view(), name="delete_product"),
               path('add_buyer/', AddBuyerView.as_view(), name="add_buyer"),
               path('buyer/<int:buyer_pk>/update_buyer', UpdateBuyerView.as_view(), name="update_buyer"),
               path('buyer/<int:buyer_pk>/delete_buyer', DeleteBuyerView.as_view(), name="delete_buyer")
               ]