import json

from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from models import Category, Product
from serializers import CategorySerializer, ProductSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework import status
import logging;
import requests
import accounts.models;

# Get an instance of a logger
logger = logging.getLogger(__name__)

PAYLOAD_CATEGORY_QUICK_REPLY = "category_"
PAYLOAD_PRODUCT_QUICK_REPLY = "product_"


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


def callSentAPI(data):
    url = 'https://graph.facebook.com/v2.6/me/messages'
    url = url + "?" + "access_token=EAAWS4fk3smoBAIyUdqQbKZCjICHwr2ZAkVhM8oDOyppnZBoJLNeQ5IjeAUrlf5X3jYV0rxvZCs0eZABSH79eCpUBHeosZBPiB3QUYrYAP7kmgwfCS6DfTQZASj05RgmFRcdjSfXaVrpnZChcvQEUH1ZBY9GFCZAJb1g87ie4uBQcNQ1QZDZD"
    requests.post(url, json=data);


def sentTextMessage(recipientId, messageText, quick_replies=None):
    data = {}
    recipient = {};

    recipient['id'] = recipientId;

    message = {}
    if messageText:
        message['text'] = messageText;
    if quick_replies:
        message['quick_replies'] = json.dumps(quick_replies)

    data['message'] = message
    data['recipient'] = recipient;

    # json_data = json.dumps(data)
    callSentAPI(data)


def receivedMessage(event):
    logger.info("Received message : ", event["message"]['mid'])

    senderId = event["sender"]["id"];

    message = event['message'];
    messageText = message["text"];

    if is_from_quick_reply(senderId, message):
        pass
    elif messageText.lower() == "menu":
        sent_store_menu(senderId);

    elif messageText == "navratan":
        sentTextMessage(senderId, messageText + ' is super awesome');
    elif messageText == "khushboo":
        sentTextMessage(senderId, messageText + " is nautanki.");
    else:
        sentTextMessage(senderId, messageText + " awesome");


def is_from_quick_reply(sender_id, message):
    if 'quick_reply' in message:

        quick_reply = message['quick_reply']

        if is_category_quick_reply(sender_id, message, quick_reply):
            return True;
        else:
            return False;


    else:
        return False;


def is_category_quick_reply(sender_id, message, quick_reply):
    if quick_reply['payload']:
        payload = quick_reply['payload'];
        if payload.startswith(PAYLOAD_CATEGORY_QUICK_REPLY, 0):
            split_array = payload.split("_");
            print "ansul" + split_array[0] + split_array[1]
            catergory_id = split_array[1]
            sent_category_product_list(sender_id, catergory_id);
            return True
    return False;


def sent_category_product_list(sender_id, catergory_id):
    product = Product.objects.filter(Category=catergory_id).all();
    quick_replies = [];
    message = ""
    for product_object in product:
        reply = {}
        reply['content_type'] = 'text'
        reply['title'] = product_object.product_name
        reply['payload'] = PAYLOAD_PRODUCT_QUICK_REPLY + str(product_object.id)
        quick_replies.append(reply)
        message = message + product_object.product_name + '\n'

    sentTextMessage(sender_id, message, quick_replies=quick_replies);


def sent_store_menu(senderId):
    # get all categoryse

    category1 = Category.objects.all()  # .only('id', 'category_name')

    quick_replies = [];
    message = ""
    for catObject in category1:
        reply = {}
        reply['content_type'] = 'text'
        reply['title'] = catObject.category_name
        reply['payload'] = PAYLOAD_CATEGORY_QUICK_REPLY + str(catObject.id)
        quick_replies.append(reply)
        message = message + catObject.category_name + '\n'

    sentTextMessage(senderId, message, quick_replies=quick_replies);


@api_view(['GET', 'POST'])
def webhook(request):
    if request.method == 'GET':

        if request.GET.get('hub.mode', '') == 'subscribe' and request.GET.get('hub.verify_token',
                                                                              "") == 'my_first_chat_bot':

            return HttpResponse(request.GET.get('hub.challenge', ''), status=status.HTTP_200_OK)
        else:
            return HttpResponse("failed", status=status.HTTP_403_FORBIDDEN)

    if request.method == 'POST':

        data = json.loads(request.body.decode("utf-8"))
        print data
        logger.info(data)

        logger.debug(" webhook Post - Data : ", data);

        if data["object"] == 'page':

            for entry in data["entry"]:

                id = entry["id"]
                time = entry["time"]

                for event in entry["messaging"]:
                    if 'sender' in event:
                        accounts.models.fetch_customers_details(event['sender']['id']);
                    if event["message"]:
                        receivedMessage(event)
                    else:
                        logger.info("Not an message event : " + event)

            return HttpResponse(status=status.HTTP_200_OK)
        else:
            logger.info("Not an page Object : ")
