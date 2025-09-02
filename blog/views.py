from django.shortcuts import render, get_object_or_404, redirect
from .models import Blog
from .forms import BlogForm
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView 
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django_filters.views import FilterView
from .filters import BlogFilter
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
import os 





class BlogListView(FilterView):
	model = Blog
	template_name = 'blog/posts_list.html'
	context_object_name = 'posts'
	filterset_class = BlogFilter
	paginate_by = 3

	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		User = get_user_model()
		context['authors'] = User.objects.all()
		return context
		
	def get_queryset(self):
		qs = super().get_queryset()
		return self.filterset_class(self.request.GET, queryset=qs).qs


class BlogDetailView(DetailView):
	model = Blog
	template_name = 'blog/post_detail.html'
	context_object_name = 'post_detail'


class BlogCreateView(LoginRequiredMixin, CreateView):
	model = Blog
	template_name = 'blog/create_post.html'
	fields = ('image','title', 'body')

	def form_valid(self, form):
		form.instance.author = self.request.user
		messages.success(self.request, "Your post published in blog !")
		return super().form_valid(form)


class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Blog
	fields = ('image', 'title', 'body') 
	template_name = 'blog/update_post.html'

	def test_func(self):
		obj = self.get_object()
		return obj.author == self.request.user

	def form_valid(self, form):
		blog = form.instance
		old_blog = Blog.objects.get(slug=blog.slug)

		if old_blog.image and blog.image != old_blog.image:
		    if os.path.isfile(old_blog.image.path):
		        os.remove(old_blog.image.path)

		messages.success(self.request, "Your post updated successfully!")
		return super().form_valid(form)



# class BlogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
# 	model = Blog
# 	template_name = 'blog/delete_post.html'
# 	success_url = reverse_lazy('posts_list')

# 	def test_func(self):
# 		obj = self.get_object()
# 		return obj.author == self.request.user

# 	def form_valid(self, form):
# 		messages.success(self.request, "Your post delete successfully!")
# 		return super().form_valid(form)






@login_required
def delete_post(request, slug):
    post = get_object_or_404(Blog, slug=slug)
    if not request.user.is_superuser and request.user.username != post.author.username:
    	return render(request, '403.html')

    if request.method == 'POST' and request.user.username == post.author.username or request.user.is_superuser:
    	if post.image:
    		image_path = post.image.path
    		if os.path.isfile(image_path):
    			os.remove(image_path)
    	post.delete()
    	messages.success(request, "Post delete successfuly !")

    return redirect('posts_list')




