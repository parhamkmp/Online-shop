from django.db import models
from django.contrib.auth import get_user_model
from shop.models import Product

CHOICES= [
	('processing', 'Processing'),
	('rejected', 'Rejected'),
	('accepted', 'Accepted'),
	('delivered', 'Delivered'),
	('returned', 'Returned'),
]

class Order(models.Model):
	user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
	recipient_name = models.CharField(max_length=100)
	postal_code = models.CharField(max_length=10)
	address = models.TextField()
	total_price = models.DecimalField(max_digits=10, decimal_places=2)
	date = models.DateTimeField(auto_now_add=True)
	status = models.CharField(
	    choices=CHOICES,
	    default='processing',
	)

	status_message = models.TextField(blank=False, null=False, default='Hello user we sent for you some messages soon')

	def __str__(self):
		return f'{self.user.username}\'s order'


class OrderItem(models.Model):
	order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField()
	color = models.CharField(max_length=20)
	price = models.DecimalField(max_digits=10, decimal_places=2)
