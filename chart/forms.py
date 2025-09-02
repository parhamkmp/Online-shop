from django import forms

class CheckOutForm(forms.Form):
	recipient_name = forms.CharField(label='recipient name', max_length=100)
	postal_code = forms.CharField(label='postal code', max_length=10)
	address = forms.CharField(label='Address', widget=forms.Textarea)
