""" @package schedule.models
This module contains the models used by the reservation system

"""

import logging
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from substations.models import Substation, Pipeline
from operators.models import *
from jsonfield import JSONField



class Reservation(models.Model):
	""" The Reservation model represents a Reservation

	Each reservation entry will contain all details needed for the time reserved by the operator. Only the 
	Operator will have access to the equipment during specified time
	"""

	substation = models.ForeignKey(Substation, help_text=_('The substation that will be used'), null=True, blank=True)

	pipeline = models.ForeignKey(Pipeline, help_text=_('The pipeline used in this reservation'), null=True, blank=True)

	start_date = models.DateField(_('start_date'), help_text=_('Start date of reservation'))
	start_time = models.TimeField(_('start_time'), help_text=_('Start time of reservation'))
	end_date = models.DateField(_('end_date'), help_text=_('End date of reservation'))
	end_time = models.TimeField(_('end_time'), help_text=_('End time of reservation'))

	operator = models.ForeignKey(StationUser, help_text=_('Operator who has access to reservation'))

	class Meta:
		verbose_name = _('reservation')
		verbose_name_plural = _('reservations')
		

	