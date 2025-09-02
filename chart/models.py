from django.db import models
from shop.models import Product
from django.contrib.auth import get_user_model


class Chart(models.Model):
	user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
	date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'{self.user.username}`s chart'

	def get_total_price_chart(self):
		return sum(item.get_total_price() for item in self.items.all())


class ChartItem(models.Model):
	chart = models.ForeignKey(Chart, on_delete=models.CASCADE, related_name='items')
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField(default=1)
	color = models.CharField(max_length=50, blank=False, null=False)

	def get_total_price(self):
		if self.product.discount_price :
			return self.product.discount_price * self.quantity
		else:
			return self.product.price * self.quantity


	def __str__(self):
		return f'{self.chart} have {self.product.name}'



