from django.contrib import admin
from .models import Chart, ChartItem

class ChartItemInline(admin.TabularInline):
	model = ChartItem
	extra = 0
	readonly_fields = ['product', 'quantity', 'color']


@admin.register(Chart)
class ChartAdmin(admin.ModelAdmin):
	list_display = ['user']
	inlines = [ChartItemInline]