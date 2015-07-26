from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import F
from forms import *
from substations.models import *
from schedule.models import *
import urllib2