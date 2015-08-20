""" @package schedule.views
This module contains top-level views for the Mercury2 scheduling utility 
"""

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import F
from django.forms import *
from substations.models import *
from tracker.forms import *
from models import *
from forms import *
from django.contrib.formtools.wizard.views import SessionWizardView
from django.http import HttpResponseRedirect
from django.shortcuts import *
import urllib
import urllib2
import json
import datetime


fetchURL_base = "http://exploration.engin.umich.edu/satops/fetchtle/api/"



def reservation_overview(request):
	""" This view returns all the reservation currently signed up for by current user """

	return render_to_response('reservations/reservation_overview.html', {'user': request.user, 'reservations': Reservation.objects.filter(operator = request.user), }, context_instance=RequestContext(request))

def substation_pipeline_select(request):
	""" This view returns the first step of the make reservation step where the user selects pipeline and substation """
	if request.method == "POST":
		form = substation_select(request.POST)
		form2 = pipeline_select(request.POST)
		form3 = time_version_select(request.POST)
		if form.is_valid() and not form2.is_valid(): 
			selection = form.cleaned_data['substation']
			form2 = pipeline_select()
			form3 = time_version_select()
			form2.fields['pipeline'].queryset = Pipeline.objects.filter(substation = selection)
			return render_to_response('reservations/schedule_step_1.html',{'user': request.user, 'form': form, 'form2': form2, 'form3': form3,}, context_instance=RequestContext(request))
		
		elif form.is_valid() and form2.is_valid() and form3.is_valid():
		 	print 'passed'
			selection_pipeline = form2.cleaned_data['pipeline']
			selection_substation = selection_pipeline.substation
			selection_user = request.user
			time_select = form3.cleaned_data['version']

			if time_select == 'pass_times':
				return redirect('reserve2B')
			else:
				return redirect('reserve2A')


			# new_reserve = Reservation(start_date = selection_start_date, substation = selection_substation, pipeline = selection_pipeline,
			# 	start_time = selection_start_time, end_date = selection_end_date, end_time = selection_end_time, operator = selection_user)
			# new_reserve.save()    
			#return render_to_response('mercury2/dashboard.html',{'user': request.user, 'reservations': Reservation.objects.filter(operator = request.user), }, context_instance=RequestContext(request))

	else:
		form = substation_select()
		form2 = pipeline_select()
		form3 = time_version_select()
	return render_to_response('reservations/schedule_step_1.html',{'user': request.user, 'form': form, 'form2':form2, 'form3':form3, }, context_instance=RequestContext(request))

def time_select_1(request):
	""" This view returns the sceond setp of make reservation step where the user sets the time here """

	if request.method == "POST":
		timeFreeForm = reservation_time_select()

		if timeFreeForm.is_valid():
			selection_start_date = timeFreeForm.cleaned_data['start_date']
			selection_start_time = timeFreeForm.cleaned_data['start_time']
			selection_end_date = timeFreeForm.cleaned_data['end_date']
			selection_end_time = timeFreeForm.cleaned_data['end_time']

			return redirect('dashboard')

	else:
		timeFreeForm = reservation_time_select()

	return render_to_response('reservations/schedule_step_2A.html', {'user': request.user, 'form3': timeFreeForm, }, context_instance=RequestContext(request))

def time_select_2(request):
	""" This view returns the second step of make reservation step where the user sets the time by selecting pass times """
	
	fetched_data = []

	proc_passes = ["N/A "]

	if request.method == "POST":
		satellite_form = satellite_select(request.POST)
		pass_form = pass_para(request.POST)
		pass_select_form = pass_select(request.POST)

		if satellite_form.is_valid() and pass_form.is_valid() and not pass_select_form.is_valid():
			selection = 'passes/'
			satellite = satellite_form.cleaned_data['satellite']
			satellite = urllib.quote_plus(satellite)
			format = '.json'
			pass_count = pass_form.cleaned_data['pass_count']
			min_elevation = pass_form.cleaned_data['min_elevation']
			ground_station = pass_form.cleaned_data['ground_station']
			show_all_passes = pass_form.cleaned_data['show_all_passes']

			api_url = str(fetchURL_base)
			api_url += str(selection) 
			api_url += str(satellite)
			api_url += str(format)
			api_url += "?pass_count="
			api_url += str(pass_count)
			api_url += "&ground_stations="
			api_url += str(ground_station)
			api_url += "&min_elevations="
			api_url += str(min_elevation)
			api_url += "&show_all_passes="
			fetched_data = urllib2.urlopen(api_url)

			#Process JSON so readable
			if format == ".json":
				fetched_data = fetched_data.read()
				#fetched_data = json.dumps(fetched_data, separators=(',', ':'))
				fetched_data = json.loads(fetched_data)				
			
			#Convert to readable string with good numbers
			if fetched_data['status']['status'] == "okay":
				proc_passes = [[]]
				proc_passes[0].append("Orbit Number  ")
				proc_passes[0].append("AOS (UTC) ")
				proc_passes[0].append("LOS (UTC) ")
				proc_passes[0].append("Elevation")
				PASS_CHOICES = []
				for passes in fetched_data['passes']:
					c_length = len(proc_passes)
					proc_passes.append([])
					proc_passes[c_length].append(str(passes.get('pass').get('orbit_number')))
					proc_passes[c_length].append(str(datetime.datetime.utcfromtimestamp(int(passes.get('pass').get('aos')))))
					proc_passes[c_length].append(str(datetime.datetime.utcfromtimestamp(int(passes.get('pass').get('los')))))
					proc_passes[c_length].append(str(passes.get('pass').get('peak_elevation')))
					PASS_CHOICES.append((str(passes.get('pass').get('orbit_number')),str(passes.get('pass').get('orbit_number'))))

			# format_form = format_type()
			# satellite_form = satellite_select()
			# pass_form = pass_para()
			# pass_select_form = pass_select()
				pass_select_form.fields['orbit'].choices = PASS_CHOICES

			return render_to_response('reservations/schedule_step_2B.html', {'user': request.user, 'satellite_form': satellite_form, 'pass_form': pass_form, 'passes': proc_passes, 'pass_select_form': pass_select_form, }, context_instance=RequestContext(request))

		elif pass_select_form.is_valid():
			# Get orbit
			selection_start_time = ''
			selection_start_date = ''
			selection_end_time = ''
			selection_end_date = ''

			orbit_select = pass_select_form.cleaned_data['passes']
			for passes in fetched_data['passes']:
				if str(passes.get('pass').get('orbit_number')) == str(orbit_select):
					AOS = datetime.datetime.utcfromtimestamp(int(passes.get('pass').get('aos')))
					LOS = datetime.datetime.utcfromtimestamp(int(passes.get('pass').get('los')))
					selection_start_time = AOS.time
					selection_start_date = AOS.date
					selection_end_time = LOS.time
					selection_end_date = LOS.date

			return redirect('dashboard')
	else:
		format_form = format_type()
		satellite_form = satellite_select()
		pass_form = pass_para()
		proc_passes = ["N/A "]
		pass_select_form = pass_select()

	return render_to_response('reservations/schedule_step_2B.html', {'user': request.user, 'satellite_form': satellite_form, 'pass_form': pass_form, 'passes': proc_passes, 'pass_select_form': pass_select_form, }, context_instance=RequestContext(request))
