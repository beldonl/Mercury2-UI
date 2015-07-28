from django.shortcuts import *
from django.template import RequestContext
from django.db.models import F
from forms import *
from substations.models import *
from schedule.models import *
import urllib
import urllib2
import json
import datetime

fetchURL_base = "http://exploration.engin.umich.edu/satops/fetchtle/api/"

def fetchTLE(request):
	""" This view returns a page to where you can get pass times and TLE's using fetchTLE """
	
	if request.method == "POST":
		resource_form = resource_type(request.POST)
		if resource_form.is_valid():
			resource = resource_form.cleaned_data['resource']
			if resource == 'sources':
				return render_to_response('tracker/sources.html')
			elif resource == 'satellites':
				return render_to_response('tracker/satellite.html')
			elif resource == 'positions':
				return render_to_response('tracker/position.html')
			elif resource == 'passes':
				return redirect('fetchTLE_passes')
			
			else:
				resource_form = resource_type() 
	else:
		resource_form = resource_type()

	return render_to_response('tracker/fetchTLE.html', {'user': request.user, 'resource_form': resource_form, }, context_instance=RequestContext(request))

def fetchTLE_sources(request):
	""" This view returns sources from fetchTLE and allows you to either download or view the data """

	return render_to_response('tracker/sources.html')

def fetchTLE_satellites(request):
	""" This view returns specific satellite TLEs from fetchTLE and allows you to either download or view the data """

	return render_response('tracker/satellite.html')

def fetchTLE_positions(request):
	""" This view returns the postions of satellites from fetchTLE and allows you to etiehr downalod or view the data"""

	return render_to_response('tracker/position.html')

def fetchTLE_passes(request):
	""" This view returns the pass times for a ground station from fetchTLE and allows you to either download or view the data"""
	if request.method == "POST":
		format_form = format_type(request.POST)
		satellite_form = satellite_select(request.POST)
		pass_form = pass_para(request.POST)

		if format_form.is_valid() and satellite_form.is_valid() and pass_form.is_valid():
			selection = 'passes/'
			satellite = satellite_form.cleaned_data['satellite']
			satellite = urllib.quote_plus(satellite)
			format = format_form.cleaned_data['format']
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
			api_url += str(show_all_passes)
			#print api_url
			fetched_data = urllib2.urlopen(api_url)

			#Process JSON so readable
			if format == ".json":
				fetched_data = fetched_data.read()
				
				#fetched_data = json.dumps(fetched_data, separators=(',', ':'))
				fetched_data = json.loads(fetched_data)				
			print fetched_data['passes'][0].get('pass').get('orbit_number')
			#Convert to readable string with good numbers
			if fetched_data['status']['status'] == "okay":
				proc_passes = [[]]
				proc_passes[0].append("Orbit Number  ")
				proc_passes[0].append("AOS (UTC) ")
				proc_passes[0].append("LOS (UTC) ")
				proc_passes[0].append("Elevation")
				for passes in fetched_data['passes']:
					c_length = len(proc_passes)
					proc_passes.append([])
					proc_passes[c_length].append(str(passes.get('pass').get('orbit_number')))
					proc_passes[c_length].append(str(datetime.datetime.utcfromtimestamp(int(passes.get('pass').get('aos')))))
					proc_passes[c_length].append(str(datetime.datetime.utcfromtimestamp(int(passes.get('pass').get('los')))))
					proc_passes[c_length].append(str(passes.get('pass').get('peak_elevation')))

			# Resend new form
			format_form = format_type()
			satellite_form = satellite_select()
			pass_form = pass_para()

			return render_to_response('tracker/passes.html', {'user': request.user, 'format_form': format_form, 'satellite_form': satellite_form, 'pass_form': pass_form, 'passes': proc_passes, }, context_instance=RequestContext(request))

	else:
		format_form = format_type()
		satellite_form = satellite_select()
		pass_form = pass_para()
		proc_passes = ["N/A "]
	return render_to_response('tracker/passes.html', {'user': request.user, 'format_form': format_form, 'satellite_form': satellite_form, 'pass_form': pass_form, 'passes': proc_passes }, context_instance=RequestContext(request))
