from django import template


register = template.Library()

@register.filter
def format_price(value):
	try:
		return '{:,}'.format(int(value))
	except (ValueError, TypeError):
		return value


@register.filter
def multiply(value, arg):
	try:
		return int(value) * int(arg)
	except (ValueError, TypeError):
		return 'ValueError / TypeError'




@register.filter
def off_price(orginal_price, discount_price):
	try:
		subtracted = int(orginal_price) - int(discount_price)
		result =  (subtracted / orginal_price) * 100
		return int(result)

	except (ValueError, TypeError):
		return 'Have Type or Value Error !'


@register.filter
def minus(num1, num2):
	try:
		result = int(num1) - int(num2)
		return result
	except (ValueError, TypeError):
		return 'Type or Value Error'