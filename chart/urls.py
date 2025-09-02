from django.urls import path
from .views import AddToChart, ChartDetailView, delete_chart_item, CheckOutView, OrderSuccessView

urlpatterns = [
	path('', ChartDetailView.as_view(), name='chart_detail'),
	path('add_to_chart/<slug:product_slug>/', AddToChart.as_view(), name='add_to_chart'),
	path('delete_item/<int:item_id>/', delete_chart_item, name='delete_item'),
	path('checkout/', CheckOutView.as_view(), name='checkout'),
	path('checkout/order_success/', OrderSuccessView.as_view(), name='order_success'),

]

