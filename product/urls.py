from django.urls import path
from product import views


app_name = 'product'

urlpatterns = [
    path('addproduct/', views.addproduct, name='addproduct'),
    path('get_product_list/', views.get_product_list, name='get_product_list'),
    path('get_filter_list/', views.get_filter_list, name='get_filter_list'),
    path('edit_product/', views.edit_product, name='edit_product'),
    path('delete_product/', views.delete_product, name='delete_product'),
    path('change_status/', views.change_status, name='change_status'),
    path('getattributename/', views.getattributename, name='getattributename'),
    path('getattributevalue/', views.getattributevalue, name='getattributevalue'),
    path('product_api/', views.ProductViewSet.as_view(), name='product_api'),
    path('product_api/<int:pro_cat_id>/', views.ProductViewSet.as_view(), name='product_api'),

]