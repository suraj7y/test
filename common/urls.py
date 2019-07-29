from django.urls import path
from common import views

app_name = 'common'

urlpatterns = [
    path('captcha/', views.captcha, name='captcha'),
    path('qr_code/', views.qr_code, name='qr_code'),
    path('add_country', views.add_country, name='add_country'),
    path('get_country_list/', views.get_country_list, name='get_country_list'),
    path('country_delete/', views.country_delete, name='country_delete'),
    path('get_saved_country/', views.get_saved_country, name='get_saved_country'),
    path('add_language', views.add_language, name='add_language'),
    path('get_language_list/', views.get_language_list, name='get_language_list'),
    path('language_delete/', views.language_delete, name='language_delete'),
    path('get_saved_language/', views.get_saved_language, name='get_saved_language'),
    path('add_city', views.add_city, name='add_city'),
    path('get_city_list/', views.get_city_list, name='get_city_list'),
    path('city_delete/', views.city_delete, name='city_delete'),
    path('get_saved_city/', views.get_saved_city, name='get_saved_city'),
    path('all_languages/', views.all_lang, name='all_lang'),
]
