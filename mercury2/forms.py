from django import forms

class addGS(forms.Form):
	title = forms.CharField()
	slug = forms.SlugField()
	longitude = forms.DecimalField()
	latitude = forms.DecimalField()
	altitude = forms.IntegerField()