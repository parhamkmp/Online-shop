from django import forms
from .models import Product, Comment

class PorductForm(forms.ModelForm):
	class Meta:
		model = Product
		fields = (
			'image_product',
			'name',
			'product_id',
			'caption',
			'price',
			'made_country',
			'color1',
			'color2',
			'color3',
			'color4',
			'color5',
			'weight',
			'height',
			'width',
		)

	widgets =  {
		'product_owner':forms.HiddenInput(),
	}




class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('writer', 'comment', 'product')
		widgets = {
			'product':forms.HiddenInput(),
			'writer':forms.HiddenInput(),
		}

