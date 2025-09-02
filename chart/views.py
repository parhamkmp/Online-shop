from django.shortcuts import render, redirect, get_object_or_404
from .models import Chart, ChartItem
from shop.models import Product
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .forms import CheckOutForm
from orders.models import Order, OrderItem
from django.views.generic import FormView
from accounts.models import CustomUser


class AddToChart(LoginRequiredMixin, View):
	def post(self, request, product_slug):
		product = get_object_or_404(Product, id=product_slug)
		chart, created = Chart.objects.get_or_create(user=request.user)
		color = request.POST.get('color')
		quantity = int(request.POST.get('quantity'))
		item, created = ChartItem.objects.get_or_create(
			chart=chart, 
			product=product,
			color=color
		)

		if not created:
			item.quantity += quantity
		else:
			item.quantity = quantity

		item.save()
		return redirect('chart_detail')
		


class ChartDetailView(LoginRequiredMixin, TemplateView):
	template_name = 'chart/detail.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		chart = Chart.objects.filter(user=self.request.user).first()
		context['chart'] = chart
		return context


@login_required
def delete_chart_item(request, item_id):
	item = get_object_or_404(ChartItem, id=item_id)
	if item.chart.user == request.user:
		item.delete()
	else:
		return render(request, '403.html')

	return redirect('chart_detail')




class CheckOutView(FormView):
	template_name = 'chart/checkout.html'
	form_class = CheckOutForm
	success_url = reverse_lazy('order_success')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		chart = Chart.objects.filter(user=self.request.user).first()
		usr = CustomUser.objects.filter(username=self.request.user)
		usrAddress = [i.address for i in usr]
		context['chart'] = chart
		context['total'] = chart.get_total_price_chart() if chart else 0
		context['usrAddress'] = str(usrAddress[0])
		return context


	def form_valid(self, form):
		chart = Chart.objects.filter(user=self.request.user).first()

		if not chart or not chart.items.exists():
			return redirect('checkout')

		order = Order.objects.create(
			user = self.request.user,
			recipient_name = form.cleaned_data['recipient_name'],
			postal_code = form.cleaned_data['postal_code'],
			address = form.cleaned_data['address'],
			total_price = chart.get_total_price_chart(), 
		)

		for item in chart.items.all():
			OrderItem.objects.create(
				order=order,
				product=item.product,
				quantity=item.quantity,
				color=item.color,
				price=item.product.price
			)
		chart.items.all().delete()
		return super().form_valid(form)


class OrderSuccessView(TemplateView):
	template_name = 'chart/order_success.html'
