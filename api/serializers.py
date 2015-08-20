from rest_framework import serializers

from substations.models import *


class SubstationSerializer(serializers.ModelSerializer):
	class Meta:
		model = Substation
		fields = ('title', 'slug', 'longitude', 'latitude', 'altitude', 'public_address', 'data_port', 'telemetry_port', 'command_port', 'commands', 'events', 'state', 'configuration')

class DeviceSerializer(serializers.ModelSerializer):

	substation = SubstationSerializer(many = True, read_only = True)

	class Meta:
		model = Device
		fields = ('title', 'device_id', 'description', 'substation', 'commands', 'events', 'state', 'configuration')

class PipelineSerializer(serializers.ModelSerializer):
	substation = SubstationSerializer(many = True, read_only = True)
	devices = DeviceSerializer(many = True, read_only = True)

	class Meta: 
		model = Pipeline
		fields = ('title', 'pipeline_id', 'description', 'substation', 'devices', 'events', 'state')


class CommandSerializer(serializers.ModelSerializer):
	class Meta:
		model = Command
		fields = ('title', 'command_id', 'description', 'metadata', 'content_type', 'object_id', 'destination')

