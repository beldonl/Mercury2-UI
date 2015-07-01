""" @package mercury2.views
This module contains top-level views for the Mercury2 user interface that don't fit with the other applications. 
"""

from django.shortcuts import render_to_response
from django.template import RequestContext
from forms import addGS

def home(request):
  """ This view is responsible for generating the Mercury2 homepage, which will be displayed to all unauthenticated
  users.
  """

  return render_to_response('mercury2/home.html')

def dashboard(request):
	""" This view returns the dashboard of the Mercury2 with ground station/substation overview 
	"""

	return render_to_response('mercury2/dashboard.html', {'user': request.user,}, context_instance=RequestContext(request)) 

def gs_overview(request):
	""" This view returns the ground station overview page """
	form = addGS()
	return render_to_response('mercury2/gs_overview.html',{'user': request.user, 'form': form, }, context_instance=RequestContext(request))