from django.shortcuts import render
from django.http import HttpResponse
from models import Category, Product
from serializers import CategorySerializer
from rest_framework.renderers import JSONRenderer

# Create your views here.

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

def index(request):

	if request.method=='GET' :
		category= Category.objects.all();
		serializer= CategorySerializer(category, many=True)
		return JSONResponse(serializer.data)

	return HttpResponse("Hello,World. You're here.")

	

