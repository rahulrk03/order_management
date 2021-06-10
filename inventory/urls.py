from django.urls import path
from .views import index, AddProductAPI, ProductList

urlpatterns = [
	path('', index,name="index"),
	path('add_product/', AddProductAPI.as_view(), name='add_product'),
	path('product_list/', ProductList.as_view(), name='product_list')
]
