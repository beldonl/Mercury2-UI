from django import forms
from substations.models import *

class addGS(forms.Form):
	title = forms.CharField()
	slug = forms.SlugField()
	longitude = forms.DecimalField()
	latitude = forms.DecimalField()
	altitude = forms.IntegerField()
	public_address = forms.CharField()
	data_port = forms.IntegerField()
	telemetry_port = forms.IntegerField()
	command_port = forms.IntegerField()

class addPipeLine(forms.Form):
	title = forms.CharField()
	pipeline_id = forms.CharField()
	description = forms.CharField()
	substation = forms.ModelChoiceField(queryset=Substation.objects.all())
	devices = forms.ModelMultipleChoiceField(queryset =Device.objects.all())

class addDevice(forms.Form):
	title = forms.CharField()
	device_id = forms.CharField()
	description = forms.CharField()
	substation = forms.ModelChoiceField(queryset=Substation.objects.all())

class GS_select(forms.Form):
	selection = forms.ModelChoiceField(queryset=Substation.objects.all())