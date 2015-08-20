from django.http import Http404
from django.http import HttpResponse

from api.serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import status

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)
@csrf_exempt
def SubstationUpdate(request):

	if request.method == 'GET':
		snippets = Substation.objects.values()
        serializer = SubstationSerializer(snippets, many=True)
        return JSONResponse(serializer.data)

	# def get(self, request, format='json'):
	# 	data = Substation.objects.all()
	# 	serializer = SubstationSerializer(data, many = True)
	# 	return JSONResponse(serializer.data)
        

	# def post(self, request, format=None):
	# 	serializer = SubstationSerializer(data=request.DATA)
	# 	if serializer.is_valid():
	# 		serializer.save()
	# 		return Response(serializer.data, status = status.HTTP_201_CREATED)
	# 	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@csrf_exempt
def PipelineUpdate(request):

	if request.method == 'GET':
		pipelines = Pipeline.objects.values()
		serializer = PipelineSerializer(pipelines, many = True)
		return JSONResponse(serializer.data)
# class PipelineConfigUpdate(APIView):

# 	def post(self, request, format=None):
# 		serializer = PipelineSerializer(data=request.DATA)
# 		if serializer.is_valid():
# 			serializer.save()
# 			return Response(serializer.data, status = status.HTTP_201_CREATED)
# 		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def DeviceUpdate(request):

	if request.method == 'GET':
		devices = Device.objects.values()
		serializer = DeviceSerializer(devices, many = True)
		return JSONResponse(serializer.data)
# class DeviceConfigUpdate(APIView):

# 	def post(self, request, format=None):
# 		serializer = DeviceSerializer(data=request.DATA)
# 		if serializer.is_valid():
# 			serializer.save()
# 			return Response(serializer.data, status = status.HTTP_201_CREATED)
# 		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommandUpdate(APIView):

	def post(self, request, format=None):
		serializer = SubstationSerializer(data=request.DATA)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status = status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)