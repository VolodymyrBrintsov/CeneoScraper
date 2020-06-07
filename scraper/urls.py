from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('extract/', views.extract, name='extract'),
    path('product-list/', views.product_list, name='product_list'),
    path('product-list/<int:product_id>/', views.product_info, name='product_info'),
    path('about/', views.about, name='about'),
]