from django.contrib import admin
from .models import Product, Comment, MainCategory, SubCategory
from mptt.admin import DraggableMPTTAdmin



class CommentLine(admin.StackedInline):
	model = Comment
	extera = 1



class ProductAdmin(admin.ModelAdmin):
	inlines = [CommentLine]




admin.site.register(Product, ProductAdmin)
admin.site.register(Comment)


admin.site.register(MainCategory, DraggableMPTTAdmin)