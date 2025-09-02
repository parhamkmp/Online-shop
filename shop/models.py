from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
import os
from django.urls import reverse
from django.utils.text import slugify
from accounts.models import CustomUser
from mptt.models import MPTTModel, TreeForeignKey

KEYWORD_CHOICES = [
    ('red', 'Red'),
    ('blue', 'Blue'),
    ('green', 'Green'),
    ('yellow', 'Yellow'),
    ('pink', 'Pink'),
    ('black', 'Black'),
    ('white', 'White'),
]


class MainCategory(MPTTModel):
    title = models.CharField(max_length=100, unique=True)
    caption = models.TextField(max_length=500)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children') 

    class MPTTMeta:
        order_insertion_by = ['title']

    class Meta:
        verbose_name = 'Main Category'
        verbose_name_plural = 'Main Categories'

    def __str__(self):
        return f'{self.title}'





class SubCategory(MPTTModel):
    title = models.CharField(max_length=100)
    main_category = models.ForeignKey(MainCategory, related_name='subcategories', on_delete=models.CASCADE)
    parent = TreeForeignKey('self',on_delete=models.CASCADE,null=True,blank=True,related_name='children')
    
    class MPTTMeta:
        order_insertion_by = ['title']

    def __str__(self):
        return self.title


class Product(models.Model):
    image_product = models.ImageField(upload_to='product_image')
    name = models.CharField(max_length=100)
    product_id = models.IntegerField(unique=True, default=0)
    caption = models.TextField(max_length=2000)
    price = models.IntegerField(default=0)
    discount_price = models.IntegerField(default=0)
    made_country = models.CharField(max_length=50)
    color1 = models.CharField(max_length=100, choices=KEYWORD_CHOICES)
    color2 = models.CharField(max_length=100, choices=KEYWORD_CHOICES, null=True, blank=True)
    color3 = models.CharField(max_length=100, choices=KEYWORD_CHOICES, null=True, blank=True)
    color4 = models.CharField(max_length=100, choices=KEYWORD_CHOICES, null=True, blank=True)
    color5 = models.CharField(max_length=100, choices=KEYWORD_CHOICES, null=True, blank=True)
    weight = models.IntegerField()
    height = models.IntegerField()
    width = models.IntegerField()
    product_owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default=1)
    slug = models.SlugField(unique=True, blank=True, null=True)
    maincategory = models.ForeignKey(MainCategory, related_name='products', on_delete=models.CASCADE, default=1)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        if self.image_product and os.path.isfile(self.image_product.path):
            os.remove(self.image_product.path)
        super().delete(*args, **kwargs)

    def clean(self):
        super().clean()
        colors = [c for c in [self.color1, self.color2, self.color3, self.color4, self.color5] if c]
        if len(colors) != len(set(colors)):
            raise ValidationError("Color must be different!")

    @property
    def colors(self):
        return [c for c in [self.color1, self.color2, self.color3, self.color4, self.color5] if c]


class Comment(models.Model):
    product = models.ForeignKey(Product, related_name='comments', on_delete=models.CASCADE)
    comment = models.TextField()
    writer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.comment[:20]) + ' ....'
