from django.urls import path
from .views import OrderChangeFormView

urlpatterns = [
	path('change/<int:pk>/', OrderChangeFormView.as_view(), name='change_order')
]