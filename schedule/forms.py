from django import forms
from substations.models import *
from django.forms.extras.widgets import SelectDateWidget
from django.db.models import Q
from models import *

class substation_select(forms.Form):
	substation = forms.ModelChoiceField(queryset=Substation.objects.all())

class pipeline_select(forms.Form):
	pipeline = forms.ModelChoiceField(queryset = Pipeline.objects.all())
	#pipeline = forms.ModelChoiceField(queryset = Pipeline.objects.all())

	# NEED TO FIX
	# def __init__(self, **kwargs):
	#     choice = kwargs.pop('selection')
	#     super(pipeline_select, self).__init__(**kwargs)
	#     if choice is not None:
	#     	self.fields['pipeline'].queryset = Pipeline.objects.filter(substation = choice)
	#     	#pipeline = forms.ChoiceField(choices = Pipeline.objects.filter(substation = choice))
		
	# def is_valid(self):
	# 	# try:
	# 	# 	pipeline_selected = Pipeline.objects.get(title = self.cleaned_data['title'])
	# 	# except Pipeline.DoesNotExist:
	# 	# 	self._erros['no_pipeline'] = 'Pipeline does not exist'
	# 	# 	return False
	# 	return True

class reservation_time_select(forms.Form):
	start_date = forms.DateField(widget = SelectDateWidget())
	start_time = forms.TimeField()
	end_date = forms.DateField(widget = SelectDateWidget())
	end_time = forms.TimeField()

	# pipeline = Pipeline()

	# def __init__(self, **kwargs):
	# 	choice = kwargs.pop('pipeline')
	# 	super(reservation_time_select, self).__init__(**kwargs)
	# 	if choice is not None:
	# 		pipeline = choice
	# 		#pipeline = forms.ChoiceField(choices = Pipeline.objects.filter(substation = choice))


	def is_valid(self, **kwargs):
		valid = super(reservation_time_select, self).is_valid()
		if not valid:
			return valid
		# Look at time to see whether time is valid
		start_date_valid = 1
		start_time_valid = 1
		end_date_valid = 1
		end_time_valid = 1
		selection_start_date = self.cleaned_data['start_date']
		selection_start_time = self.cleaned_data['start_time']
		selection_end_date = self.cleaned_data['end_date']
		selection_end_time = self.cleaned_data['end_time']
		for reservations in Reservation.objects.all():
			# First look at start time
			if selection_start_date > reservations.start_date and selection_start_date < reservations.end_date:
				start_date_valid = 0
				end_date_valid = 0
				start_time_valid = 0
				end_time_valid = 0
			if selection_start_date == reservations.start_date:
				if selection_start_time >= reservations.start_time:
					start_time_valid = 0
			if selection_start_date == reservations.end_date:
				if selection_start_time < reservations.end_time:
					start_time_valid = 0
			if selection_end_date > reservations.end_date and selection_end_date < reservations.end_date: 
				end_date_time_valid = 0
			if selection_end_date == reservations.start_date:
				if selection_end_time >= reservations.start_time:
					end_time_valid = 0
			print start_time_valid + start_date_valid + end_date_valid + end_time_valid
			self._errors['start_time'] = "Time error"
			if start_date_valid + end_date_valid + start_time_valid + end_time_valid < 4:
				if start_date_valid == 0 and end_date_valid == 0 and start_time_valid == 0 and end_time_valid == 0:
					self._errors['Time_Slot_Error'] = 'Time slot is taken'
				elif start_date_valid == 0:
					self._errors['Start_Date_Error'] = 'Start date is in middle of previous reservation'
				elif start_time_valid == 0:
					self._errors['Start_Time_Error'] = 'Start time is in conflict'
				elif end_date_valid == 0:
					self._errors['End_Date_Error'] = 'End date is in conflict'
				else:
					self._errors['End_Time_Error'] = 'End time is in middle of future reservation'
				return False
		return True


