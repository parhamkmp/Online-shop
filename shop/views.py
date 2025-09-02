from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Comment
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, CreateView 
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic.edit import FormMixin
from .forms import CommentForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import os
from accounts.models import CustomUser
from .filters import ProductFilter
from django.contrib.auth import get_user_model
from django_filters.views import FilterView



class ProductListView(FilterView):
	model = Product
	template_name = 'shop/products_list.html'
	context_object_name = 'products'
	filterset_class = ProductFilter
	paginate_by = 3

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		User = get_user_model()
		context['product_owner'] = User.objects.all()
		return context

	def get_queryset(self):
		qs = super().get_queryset()
		return self.filterset_class(self.request.GET, queryset=qs).qs






class ProductDetailView(FormMixin, DetailView):
	model = Product
	template_name = 'shop/products_detail.html'
	context_object_name = 'product'
	form_class = CommentForm

	def get_success_url(self):
		return reverse('product_detail', kwargs={'slug':self.object.slug})

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['form'] = CommentForm(initial={'product':self.object, 'writer':self.request.user})
		return context

	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		form = self.get_form()
		if form.is_valid():
			return self.form_valid(form)
		return self.form_invalid(form)

	def form_valid(self, form):
		comment = form.save(commit=False)
		comment.product = self.object
		comment.writer = self.request.user
		comment.save()
		return super().form_valid(form)



@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == 'POST' and request.user in [comment.writer, comment.product.product_owner]:
        comment.delete()
    return redirect('product_detail', slug=comment.product.slug)



class ProductCreateView(LoginRequiredMixin,CreateView):
	model = Product
	template_name = 'shop/create_product.html'
	fields = (
			'image_product',
			'name',
			'product_id',
			'caption',
			'price',
			'discount_price',
			'made_country',
			'color1',
			'color2',
			'color3',
			'color4',
			'color5',
			'weight',
			'height',
			'width',
			'maincategory',
		)

	def form_valid(self, form):
		form.instance.product_owner = self.request.user
		messages.success(self.request, "Your product list in shop for sale !")
		return super().form_valid(form)






class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Product
	template_name = 'shop/update_product.html'
	fields = (
			'image_product',
			'name',
			'caption',
			'price',
			'discount_price',
			'made_country',
			'color1',
			'color2',
			'color3',
			'color4',
			'color5',
			'weight',
			'height',
			'width',
			'maincategory',
		)

	def test_func(self):
		obj = self.get_object()
		return obj.product_owner == self.request.user

	def form_valid(self, form):
		product = form.instance
		old_product = Product.objects.get(slug=product.slug)

		if old_product.image_product and product.image_product != old_product.image_product:
			if os.path.isfile(old_product.image_product.path):
				os.remove(old_product.image_product.path)

		messages.success(self.request, "Your product info updated !")
		return super().form_valid(form)
		


@login_required
def delete_product(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.user != product.product_owner:
    	return render(request, '403.html')

    if request.method == 'POST' and request.user.username == product.product_owner.username:
    	if product.image_product:
    		image_path = product.image_product.path
    		if os.path.isfile(image_path):
    			os.remove(image_path)
    	product.delete()
    	messages.success(request, "Product delete successfuly !")

    return redirect('products_list')