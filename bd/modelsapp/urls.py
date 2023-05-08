from django.urls import path

from .views import *

urlpatterns = [path('list_products/', ListProducts.as_view(), name="list_products"),
               path('', index_view, name="home"),
               path('product/<int:pk>/', ProductViews.as_view(), name="product"),
               path('list_buyers/', list_buyer_view, name="list_buyers"),
               path('buyer/<int:buyer_pk>/', detail_buyer_view, name="buyer"),
               path('buyer/<int:buyer_pk>/product/<int:pk>', delete_product_view, name="delete_product")
               ]