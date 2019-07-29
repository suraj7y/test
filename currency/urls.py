from django.urls import path
from currency import views


app_name = 'currency'

urlpatterns = [
    path('', views.add_currency, name='add_currency'),
    path('get_currency_list/', views.get_currency_list, name='get_currency_list'),
    path('currency_delete/', views.currency_delete, name='currency_delete'),
    path('get_saved_currency/', views.get_saved_currency, name='get_saved_currency'),
]