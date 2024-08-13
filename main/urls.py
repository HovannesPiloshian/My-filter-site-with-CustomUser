from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('cart/', views.view_cart, name='cart'),
    path('add-to-cart/<int:tent_id>/', views.add_to_cart, name='add_to_cart'),
]
