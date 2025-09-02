from django.contrib import admin
from .models import Order, OrderItem
from django.core.mail import send_mail
from django.conf import settings


class OrderItemInline(admin.TabularInline):  
    model = OrderItem
    extra = 0  
    readonly_fields = ['product', 'quantity', 'color', 'price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'id', 'address', 'formatted_price', 'date', 'status']
    inlines = [OrderItemInline]

    def formatted_price(self, obj):
        return f'$ {obj.total_price:,.0f}'
    formatted_price.short_description = 'Total price' 

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if obj.status in ['accepted', 'rejected', 'delivered', 'returned'] and obj.status_message:
            subject = f'Your order status: {obj.get_status_display()}'
            message = f'''Hello dear {obj.recipient_name},\n
Your order status: {obj.get_status_display()}
Explanation of the store manager:
{obj.status_message}
with respect،
store manager
            '''

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [obj.user.email],
                fail_silently=True
            )
