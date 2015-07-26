""" @package schedule.views
This module contains top-level views for the Mercury2 scheduling utility 
"""

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import F
from django.forms import *
from substations.models import *
from models import *
from forms import *
from django.contrib.formtools.wizard.views import SessionWizardView
from django.http import HttpResponseRedirect




# Form Wizard for scheduler implemented here

# FORMS = [("substation", substation_select), ("pipeline", pipeline_select), ("start_time", start_time_select)
# , ("end_time", end_time_select)]

# TEMPLATES = {"substation": "reservations/substation_select.html", "pipeline": "reservations/pipeline_select.html", "start_time": "reservations/start_time_select.html", "end_time": "reservations/end_time_select.html"}

# class ReservationWizard(SessionWizardView):
# 	def get_template_names(self):
# 		return [TEMPLATES[self.steps.current]]

# 	def done(self, form_list, **kwargs):
# 		return 0
def reservation_overview(request):
	""" This view returns all the reservation currently signed up for by current user """

	return render_to_response('reservations/reservation_overview.html', {'user': request.user, 'reservations': Reservation.objects.filter(operator = request.user), }, context_instance=RequestContext(request))

def substation_pipeline_select(request):
	""" This view returns the ground station overview page, gives users details of each substation"""
	if request.method == "POST":
		form = substation_select(request.POST)
		form2 = pipeline_select(request.POST)
		form3 = reservation_time_select(request.POST or None, request.FILES or None)

		if form.is_valid() and form2.is_valid() and not form3.is_valid():
			selection = form.cleaned_data['substation']

			form2.fields['pipeline'].queryset = Pipeline.objects.filter(substation = selection)
			return render_to_response('reservations/schedule_step_1.html',{'user': request.user, 'form': form, 'form2': form2, 'form3': form3, }, context_instance=RequestContext(request))
		

		if form.is_valid() and not form2.is_valid(): 
			selection = form.cleaned_data['substation']
			form2 = pipeline_select()
			form2.fields['pipeline'].queryset = Pipeline.objects.filter(substation = selection)
			form3 = reservation_time_select()
			return render_to_response('reservations/schedule_step_1.html',{'user': request.user, 'form': form, 'form2': form2, 'form3': form3, }, context_instance=RequestContext(request))
		
		elif form.is_valid() and form2.is_valid() and form3.is_valid():
		 	print 'passed'
			selection_pipeline = form2.cleaned_data['pipeline']
			selection_substation = selection_pipeline.substation
			selection_start_date = form3.cleaned_data['start_date']
			selection_start_time = form3.cleaned_data['start_time']
			selection_end_date = form3.cleaned_data['end_date']
			selection_end_time = form3.cleaned_data['end_time']
			selection_user = request.user


			new_reserve = Reservation(start_date = selection_start_date, substation = selection_substation, pipeline = selection_pipeline,
				start_time = selection_start_time, end_date = selection_end_date, end_time = selection_end_time, operator = selection_user)
			new_reserve.save()    
			return render_to_response('mercury2/dashboard.html',{'user': request.user, 'reservations': Reservation.objects.filter(operator = request.user), }, context_instance=RequestContext(request))

	else:
		form = substation_select()
	return render_to_response('reservations/schedule_step_1.html',{'user': request.user, 'form': form,}, context_instance=RequestContext(request))
	