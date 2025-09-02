import os
from django.shortcuts import render
from django.views.generic import CreateView
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from blog.models import Blog
from shop.models import Product
from django.views.generic.edit import UpdateView
from .forms import EditProfileForm
from django.contrib import messages
from .models import CustomUser
from orders.models import Order
from django.core.paginator import Paginator


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'registration/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        orders_qs = Order.objects.filter(user=self.request.user).order_by('-date')
        orders_superuser_qs = Order.objects.all().order_by('-date')

        page_number = self.request.GET.get('page', 1)

        orders_paginator = Paginator(orders_qs, 3)  
        orders_page = orders_paginator.get_page(page_number)

        superuser_orders_page = None
        if self.request.user.is_staff or self.request.user.role == 'admin':
            superuser_orders_paginator = Paginator(orders_superuser_qs, 3)
            superuser_orders_page = superuser_orders_paginator.get_page(page_number)



        context['user'] = self.request.user
        context['recent_posts'] = Blog.objects.filter(author=self.request.user).order_by('-last_update')[:5]
        context['recent_products'] = Product.objects.filter(product_owner=self.request.user).order_by('name')

        context['orders_page'] = orders_page
        context['superuser_orders_page'] = superuser_orders_page

        return context


class EditProfileView(LoginRequiredMixin, UpdateView):
    form_class = EditProfileForm
    template_name = 'registration/edit_profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user


    def form_valid(self, form):
        user = form.instance
        old_user = CustomUser.objects.get(pk=user.pk)

        if old_user.image_profile and user.image_profile != old_user.image_profile:
            if os.path.isfile(old_user.image_profile.path):
                os.remove(old_user.image_profile.path)

        messages.success(self.request, "Your profile update successfuly!")
        return super().form_valid(form)
