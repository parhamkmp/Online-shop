from .forms import OrderChangeForm
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from .models import Order
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin



class OrderChangeFormView(LoginRequiredMixin,UpdateView):
	model = Order
	form_class = OrderChangeForm
	success_url = reverse_lazy('home')
	template_name = 'orders/order_change_form.html'

	def test_func(self):
		obj = self.get_object()
		return obj.user.username == self.request.user


	def form_valid(self, form):
		order = form.save(commit=False)
		order.save()
		if order.status in ['accepted', 'rejected', 'delivered', 'returned'] and order.status_message:
			subject = f'Your order status: {order.get_status_display()}'
			message = f'''Hello dear {order.recipient_name},\n
Your order status: {order.get_status_display()}
Explanation of the store manager:
{order.status_message}
with respect,
store manager
'''
			send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [order.user.email],
                fail_silently=True
            )


		return super().form_valid(form)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['order'] = self.object
		return context

