from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from models import Category, Product
from serializers import CategorySerializer, ProductSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework import status
import logging;

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@api_view(['GET', 'POST'])
def category(request):
    if request.method == 'GET':
        category = Category.objects.all();
        serializer = CategorySerializer(category, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data);
        if serializer.is_valid():
            serializer.save();
            return Response(serializer.data, status=status.HTTP_201_CREATED);
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def productlist(request):
    if request.method == 'GET':
        product = Product.objects.all()
        serializer = ProductSerializer(product, many=True)
        return JSONResponse(serializer.data)


def index(request):
    return HttpResponse('<pre>' + 'Anshul' + '</pre>')


def receivedMessage(event):
    logger.info("Received message : " + event)


@api_view(['GET', 'POST'])
def webhook(request):
    if request.method == 'GET':

        if request.GET.get('hub.mode', '') == 'subscribe' and request.GET.get('hub.verify_token',
                                                                              "") == 'my_first_chat_bot':

            return HttpResponse(request.GET.get('hub.challenge', ''), status=status.HTTP_200_OK)
        else:
            return HttpResponse("failed", status=status.HTTP_403_FORBIDDEN)

    if request.method == 'POST':

        data = request.body
        logger.info(" webhook Post - Data : " + data);

        if data.object == 'page':

            for entry in data.entry:

                id = entry.id
                time = entry.time

                for event in entry.messaging:
                    if event.message:
                        receivedMessage(event)
                    else:
                        logger.info("Not an message event : " + event)

            return HttpResponse()
        else :
            logger.info("Not an page Object : ")

