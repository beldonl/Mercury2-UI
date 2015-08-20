from django import forms
from substations.models import *
from django.forms.extras.widgets import SelectDateWidget
from django.db.models import Q

RESOURCE_CHOICES = (
    ('sources', 'Sources'),
    ('satellites', 'Satellites'),
    ('positions', 'Positions'), 
    ('passes', 'Passes'),)

FORMAT_CHOICES = (
	('.json', 'JSON'),
	('.xml', 'XML'),
	('.jsonp', 'JSONP'),
	('.txt', 'TEXT'),)

GS_CHOICES = (
	('MXL', 'MXL'),
	('SRI', 'SRI'),
	('Australia', 'Australia'),
	('NewZealand', 'New Zealand'),
	('Tokyo', 'Tokyo'),
	('NorthCarolina', 'North Carolina'),
	('Colorado', 'Colorado'),
	('Alaska', 'Alaska'),
	('Kitakyushu', 'Kitakyushu'),
	('Netherlands', 'Netherlands'),
	('JPL', 'JPL'),)

TF = (
	('true', 'True'),
	('false', 'False'),)


class resource_type(forms.Form):
	resource = forms.ChoiceField(choices=RESOURCE_CHOICES)

class format_type(forms.Form):
	format = forms.ChoiceField(choices=FORMAT_CHOICES)

class satellite_select(forms.Form):
	satellite = forms.CharField()

# Sources

# Positions

# Satellites

# Passes
class pass_para(forms.Form):
	pass_count = forms.IntegerField()
	ground_station = forms.ChoiceField(choices=GS_CHOICES)
	min_elevation = forms.IntegerField()
	show_all_passes = forms.ChoiceField(choices=TF)
