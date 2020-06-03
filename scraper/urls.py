from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.extract, name='extract'),
    path('result/', views.extract_result, name='extract_result')
]