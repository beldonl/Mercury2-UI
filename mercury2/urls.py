""" @package mercury2.urls
This package defines the top-level URL routes for the Mercury2 user interface.
"""

from django.conf.urls import patterns, include, url
from django.contrib import admin

from django.conf.urls import patterns
from schedule.forms import *
from schedule.views import *
from tracker.views import *

#from administration.admin import mercury2_admin

admin.autodiscover()

urlpatterns = patterns('',
  url(r'^$', 'mercury2.views.home', name='home'),
  url(r'^users/', include('allauth.urls')),
  url(r'^admin/', include(admin.site.urls)),
  url(r'^dashboard/', 'mercury2.views.dashboard', name='dashboard'),
  url(r'^gs_overview/', 'mercury2.views.gs_overview', name='gs_overview'),
  url(r'^gs_edit/', 'mercury2.views.gs_edit', name='gs_edit'),
  url(r'^reservation_overview/', 'schedule.views.reservation_overview', name='reservation_overview'),
  #url(r'^reserve/', ReservationWizard.as_view(FORMS), name='reserve'),
  url(r'^fetchtle/', 'tracker.views.fetchTLE', name='fetchTLE'),
  url(r'^passes/', 'tracker.views.fetchTLE_passes', name = 'fetchTLE_passes'),


  url(r'^reserve/', 'schedule.views.substation_pipeline_select', name='reserve'),
  #url(r'^admin/', include(mercury2_admin.urls)),
)
