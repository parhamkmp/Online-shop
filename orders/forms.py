from django import forms
from .models import Order, OrderItem

class OrderChangeForm(forms.ModelForm):
	class Meta:
		model = Order
		fields = ('status', 'status_message')

