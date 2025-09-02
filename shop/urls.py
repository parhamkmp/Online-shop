from django.urls import path
from .views import ProductListView, ProductDetailView, ProductCreateView, delete_comment, ProductUpdateView, delete_product

urlpatterns = [
	path('', ProductListView.as_view(), name='products_list'),
	path('products/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
	path('product/create_product/', ProductCreateView.as_view(), name='product_create'),
	path('comment/delete/<int:pk>/', delete_comment, name='delete_comment'),
	path('products/<slug:slug>/delete/', delete_product, name='delete_product'),
	path('products/<slug:slug>/update/', ProductUpdateView.as_view(), name='product_update'),
]