""" @package mercury2.views
This module contains top-level views for the Mercury2 user interface that don't fit with the other applications. 
"""

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import F
from forms import *
from substations.models import *


def home(request):
  """ This view is responsible for generating the Mercury2 homepage, which will be displayed to all unauthenticated
  users.
  """

  return render_to_response('mercury2/home.html')

def dashboard(request):
	""" This view returns the dashboard of the Mercury2 with ground station/substation overview 
	"""

	return render_to_response('mercury2/dashboard.html', {'user': request.user,}, context_instance=RequestContext(request)) 

def gs_edit(request):
	""" This view returns the ground station overview page , allows users to add new substation for now"""

	if request.method == 'POST':
		# form1 = addGS(request.POST)
		# if form.is_valid():
		# 	title = form.cleaned_data['title']
		# 	slug = form.cleaned_data['slug']
		# 	longitude = form.cleaned_data['longitude']
		# 	latitude = form.cleaned_data['latitude']
		# 	altitude = form.cleaned_data['altitude']
		# 	public_address = form.cleaned_data['public_address']
		# 	data_port = form.cleaned_data['data_port']
		# 	telemetry_port = form.cleaned_data['telemetry_port']
		# 	command_port = form.cleaned_data['command_port']
		# 	p = Substation(title = title, slug = slug, longitude = longitude, latitude = latitude,
		# 		altitude = altitude, public_address = public_address, data_port = data_port, 
		# 		telemetry_port = telemetry_port, command_port = command_port,)
		# 	p.save()

		# form = addPipeLine(request.POST)
		# if form.is_valid():
		# 	title = form.cleaned_data['title']
		# 	pipeline_id = form.cleaned_data['pipeline_id']
		# 	description = form.cleaned_data['description']
		# 	substation = form.cleaned_data['substation']
		# 	p = Pipeline(title = title, pipeline_id = pipeline_id, description = description, substation = substation,
		# 		)
		# 	p.save()
			

		form = addDevice(request.POST)
		if form.is_valid():
			title = form.cleaned_data['title']
			device_id = form.cleaned_data['device_id']
			description = form.cleaned_data['description']
			substation = form.cleaned_data.get('substation')
			p = Device(title = title, device_id = device_id, description = description, substation = substation)
			p.save()
	else:
		form = addDevice()
	return render_to_response('mercury2/gs_edit.html',{'user': request.user, 'form': form, 'substations': Substation.objects.values(), 
		'pipelines': Pipeline.objects.values(), 'Devices': Device.objects.values(), }, context_instance=RequestContext(request))

def gs_overview(request):
	""" This view returns the ground station overview page, gives users details of each substation"""
	if request.method == "POST":
		form = GS_select(request.POST)
		if form.is_valid():
			selection = form.cleaned_data['selection']
			devicesFiltered = Device.objects.filter(substation = selection)
			pipelinesFiltered = Pipeline.objects.filter(substation = selection)
			return render_to_response('mercury2/gs_overview.html',{'user': request.user, 'form': form, 'substations': Substation.objects.values(),
			 'pipelines': pipelinesFiltered, 'Devices': devicesFiltered, 'current' : selection }, context_instance=RequestContext(request))
	else:
		form = GS_select()
	return render_to_response('mercury2/gs_overview.html',{'user': request.user, 'form': form, 'substations': Substation.objects.values(), 
		'pipelines': Pipeline.objects.values(), 'Devices': Device.objects.values(), }, context_instance=RequestContext(request))




