from django.urls import path
from category import views

app_name = 'category'

urlpatterns = [

    path('', views.category, name='category'),
    path('category_list/', views.category_list, name='category_list'),
    path('category_operations/', views.category_operations, name='category_operations'),
    path('category_delete/', views.category_delete, name='category_delete'),
    path('get_category/', views.get_category, name='get_category'),

    path('get_saved_category/', views.get_saved_category, name='get_saved_category'),
    path('get_category_list/', views.get_category_list, name='get_category_list'),

    path('get_filter_list/', views.get_filter_list, name='get_filter_list'),
    path('filter_operations/', views.filter_operations, name='filter_operations'),
    path('filter_delete/', views.filter_delete, name='filter_delete'),
    path('get_saved_filter/', views.get_saved_filter, name='get_saved_filter'),

    path('get_filter_value_list/', views.get_filter_value_list, name='get_filter_value_list'),
    path('filter_value_operations/', views.filter_value_operations, name='filter_value_operations'),
    path('filter_value_delete/', views.filter_value_delete, name='filter_value_delete'),
    path('get_saved_filter_values/', views.get_saved_filter_values, name='get_saved_filter_values'),

    path('get_saved_img/', views.get_saved_img, name='get_saved_img'),
    path('del_img/', views.del_img, name='del_img'),

    path('approve_filter/', views.approve_filter, name='approve_filter'),
    path('reject_filter/', views.reject_filter, name='reject_filter'),

]
