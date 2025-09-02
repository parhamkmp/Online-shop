from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.text import slugify
import os


class Blog(models.Model):
	title = models.CharField(max_length=50, null=False, blank=False, unique=True)
	body  = models.TextField(max_length=1000, null=False, blank=False)
	image = models.ImageField(upload_to='blog_img', blank=False, null=False, unique=True)
	date = models.DateTimeField(auto_now_add=True)
	last_update = models.DateTimeField(auto_now=True) 
	author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
	slug = models.SlugField(unique=True, blank=True)


	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.title)
		super().save(*args, **kwargs)


	def get_absolute_url(self):
		return reverse('post_detail', kwargs={'slug': self.slug})

	def __str__(self):
		return self.title

	def delete(self, *args, **kwargs):
		if self.image and os.path.isfile(self.image.path):
			os.remove(self.image.path)
		super().delete(*args, **kwargs)




