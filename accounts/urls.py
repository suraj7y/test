from django.urls import path
from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('registration/', views.register, name='register'),
    path('verification/', views.verification, name='verification'),
    path('login/', views.user_login, name='user_login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password/', views.reset_password, name='reset_password'),
    #path('index/', views.index, name='index'),
]