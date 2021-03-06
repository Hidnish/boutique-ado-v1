from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_products, name='products'),
    # django selects first matchin pattern available and would not distinguish 
    # a product number and a string like 'add'
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('add/', views.add_product, name='add_product'),
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete/<int:product_id>/', views.delete_product, name='delete_product'),
]
