""" @package mercury2.views
This module contains top-level views for the Mercury2 user interface that don't fit with the other applications. 
"""

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import F
from forms import *
from substations.models import *
from schedule.models import *



def home(request):
  """ This view is responsible for generating the Mercury2 homepage, which will be displayed to all unauthenticated
  users.
  """

  return render_to_response('mercury2/home.html')

def dashboard(request):
	""" This view returns the dashboard of the Mercury2 with ground station/substation overview 
	"""

	return render_to_response('mercury2/dashboard.html', {'user': request.user, 'reservations': Reservation.objects.filter(operator = request.user), } , context_instance=RequestContext(request)) 

def gs_edit(request):
	""" This view returns the ground station overview page , allows users to add new substation for now"""

	if request.method == 'POST':
		
		
		form1 = addGS(request.POST)
		form2 = addPipeLine(request.POST)
		form3 = addDevice(request.POST)

		if form1.is_valid():
			title = form1.cleaned_data['title']
			slug = form1.cleaned_data['slug']
			longitude = form1.cleaned_data['longitude']
			latitude = form1.cleaned_data['latitude']
			altitude = form1.cleaned_data['altitude']
			public_address = form1.cleaned_data['public_address']
			data_port = form1.cleaned_data['data_port']
			telemetry_port = form1.cleaned_data['telemetry_port']
			command_port = form1.cleaned_data['command_port']
			p = Substation(title = title, slug = slug, longitude = longitude, latitude = latitude,
				altitude = altitude, public_address = public_address, data_port = data_port, 
				telemetry_port = telemetry_port, command_port = command_port,)
			p.save()

		if form2.is_valid():
			title = form2.cleaned_data['title']
			pipeline_id = form2.cleaned_data['pipeline_id']
			description = form2.cleaned_data['description']
			substation = form2.cleaned_data['substation']
			p = Pipeline(title = title, pipeline_id = pipeline_id, description = description, substation = substation,
				)
			p.save()
		if form3.is_valid():
			title = form3.cleaned_data['title']
			device_id = form3.cleaned_data['device_id']
			description = form3.cleaned_data['description']
			substation = form3.cleaned_data.get('substation')
			p = Device(title = title, device_id = device_id, description = description, substation = substation)
			p.save()
	else:
		form1 = addGS()
		form2 = addPipeLine()
		form3 = addDevice()
	return render_to_response('mercury2/gs_edit.html',{'user': request.user, 'form1': form1, 'form2': form2, 'form3': form3,  }, context_instance=RequestContext(request))

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














