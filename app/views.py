import json
import logging;

import requests
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

import accounts.models;
import cart.models as cart_models;
from app import logic
from app.postback import received_postback
from models import Category, Product
from serializers import CategorySerializer, ProductSerializer
from address.models import Addresses, CustomerAddress
from store.models import get_stores, Store, connect_store_to_customer
import store.models as store_models;
from const import *
# from fbcalls import *
import fbcalls
import quick_reply as quick_r

# Get an instance of a logger
logger = logging.getLogger(__name__)


# PAYLOAD_CATEGORY_QUICK_REPLY = "category_"
# PAYLOAD_PRODUCT_QUICK_REPLY = "product_"
# PAYLOAD_STORE_QUICK_REPLY = "store_"


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


def received_message(event):
    logger.info("Received message : ", event["message"]['mid'])

    sender_id = event["sender"]["id"];

    message = event['message'];
    if is_from_quick_reply(sender_id, message):
        return;
    elif is_has_attachment(sender_id, message):
        return;

    if 'text' in message:
        messageText = message["text"];
    else:
        return

    if messageText.lower() == "menu":
        sent_store_menu(sender_id);
    elif messageText.lower() == "cart":
        logic.show_user_cart(sender_id)
    elif messageText.lower() == 'location':
        fetch_customer_location(sender_id)
    else:
        fbcalls.sentTextMessage(sender_id, messageText + " awesome");


def is_from_quick_reply(sender_id, message):
    if 'quick_reply' in message:

        quick_reply = message['quick_reply']

        if is_category_quick_reply(sender_id, message, quick_reply):
            return True;
        elif is_product_quick_reply(sender_id, message, quick_reply):
            return True;
        elif is_select_store_quick_reply(sender_id, message, quick_reply):
            return True;
        elif quick_r.is_ignore_qr(sender_id, message, quick_reply):
            return True
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


def is_product_quick_reply(sender_id, message, quick_reply):
    if quick_reply['payload']:
        payload = quick_reply['payload'];
        if payload.startswith(PAYLOAD_PRODUCT_QUICK_REPLY, 0):
            split_array = payload.split("_");
            print "Product quick " + split_array[0] + split_array[1]
            product_id = split_array[1]
            logic.add_product_to_cart(sender_id, product_id);
            return True
    return False;


def is_select_store_quick_reply(sender_id, message, quick_reply):
    if quick_reply['payload']:
        payload = quick_reply['payload'];
        if payload.startswith(PAYLOAD_STORE_QUICK_REPLY, 0):
            split_array = payload.split("_");
            print "Quick reply : store id" + split_array[0] + split_array[1]
            store_id = split_array[1]
            map_store_to_customer(sender_id, store_id);
            return True
    return False;


def map_store_to_customer(sender_id, store_id):
    customer = accounts.models.fetch_customers_details(sender_id)

    connect_store_to_customer(store_id, customer);

    # show store menu

    sent_store_menu(sender_id);


def sent_category_product_list(sender_id, catergory_id):
    # get customers
    customer = accounts.models.fetch_customers_details(sender_id)

    store = store_models.get_customers_store(customer);
    store_product = store_models.StoreProducts.objects.filter(store=store, product__Category__id=catergory_id);

    # product = Product.objects.filter(Category=catergory_id).all();
    quick_replies = [];
    message = ""
    for product_object in store_product:
        reply = {}
        reply['content_type'] = 'text'
        reply['title'] = product_object.product.product_name
        reply['payload'] = PAYLOAD_PRODUCT_QUICK_REPLY + str(product_object.product.id)
        quick_replies.append(reply)
        message = message + product_object.product.product_name + '\n'

    fbcalls.sentTextMessage(sender_id, message, quick_replies=quick_replies);


def sent_store_menu(senderId):
    # get customers
    customer = accounts.models.fetch_customers_details(senderId);

    # get customer's store
    try:
        store = store_models.get_customers_store(customer);
    except store_models.StoreCustomer.DoesNotExist:
        message = "You have not selected any food place."
        fbcalls.sentTextMessage(senderId, message);
        logic.ask_for_user_location(senderId);
        return;

    # get store category
    cat = store_models.get_store_category(store)

    # category1 = Category.objects.all()  # .only('id', 'category_name')
    for catObject in cat:
        print "Anshul cat ; " + str(catObject)

    # show generic template for menu (max element limit 10 (fb limit), ignoring this for now[POC])

    attachment = {}
    attachment['type'] = "template"
    payload = {};
    payload['template_type'] = "generic"
    payload['image_aspect_ratio'] = "square"

    elements = [];

    for catObject in cat:
        p_category = catObject.product.Category;
        element = {};
        element['title'] = p_category.category_name;
        element[
            'image_url'] = 'https://scontent.fdel1-2.fna.fbcdn.net/v/t31.0-8/16819206_1205196312912955_6951350097360556394_o.jpg?oh=70a9f22a3ed31ed7dc8908e3ac347970&oe=5926FE3D'

        button = {};
        button['type'] = 'postback'
        button['title'] = 'Show Products'
        button['payload'] = PAYLOAD_CATEGORY_QUICK_REPLY + str(p_category.id)

        buttons = [];
        buttons.append(button)

        element['buttons'] = buttons;
        elements.append(element);

    payload['elements'] = elements;
    attachment['payload'] = payload;

    # quick_replies = [];
    # message = ""
    # for catObject in cat:
    #     reply = {}
    #     reply['content_type'] = 'text'
    #     reply['title'] = catObject.product.Category.category_name;
    #     reply['payload'] = PAYLOAD_CATEGORY_QUICK_REPLY + str(catObject.product.Category.id)
    #     quick_replies.append(reply)
    #     message = message + catObject.product.Category.category_name + '\n'

    message = "Please select category - "
    fbcalls.sentTextMessage(senderId, attachment=attachment);


def fetch_customer_location(sender_id):
    quick_replies = [];
    message = "Please share your location:"
    reply = {}
    reply['content_type'] = 'location'
    quick_replies.append(reply)
    fbcalls.sentTextMessage(sender_id, message, quick_replies=quick_replies);


def is_has_attachment(sender_id, message):
    if 'attachments' in message:

        attachments = message['attachments']

        for attachment in attachments:
            handle_attachment(sender_id, message, attachment)
        return True
    else:
        return False


def handle_attachment(sender_id, message, attachment):
    type = attachment['type'];
    if type == "location":
        handle_customer_location(sender_id, message, attachment)


def handle_customer_location(sender_id, message, attachment):
    coordinates = attachment['payload']['coordinates'];
    lat = coordinates['lat']
    longitude = coordinates['long'];
    title = attachment['title']

    address = Addresses(title=title, latitude=lat, longitude=longitude);
    address.save();

    # get user
    customer = accounts.models.fetch_customers_details(sender_id);

    # add customer address
    customer_address = CustomerAddress(user=customer, address=address);
    customer_address.create_customer_address();

    # get near stores
    nearby_stores = get_stores(lat, longitude);
    show_nearby_stores(sender_id, nearby_stores);

    print "lat : " + str(lat) + "longitude : " + str(longitude)


def show_nearby_stores(sender_id, stores):
    if stores is not None and len(stores) > 0:
        # sort stores based on distance (Min on priority )
        message = "";
        q_reply = [];
        for store in stores:
            reply = {}
            reply['content_type'] = 'text'
            reply['title'] = store.name
            reply['payload'] = PAYLOAD_STORE_QUICK_REPLY + str(store.id)
            q_reply.append(reply)
            message = message + store.name + '\n'
        fbcalls.sentTextMessage(sender_id, message, quick_replies=q_reply);

    else:
        print stores;
        sent_no_store_found(sender_id)


def sent_no_store_found(sender_id):
    fbcalls.sentTextMessage(sender_id, "No store found,in your location");


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
                    if 'message' in event and event["message"]:
                        received_message(event)
                    else:
                        logger.info("Not an message event : " + str(event))

                    # postback url call
                    if 'postback' in event and event['postback']:
                        received_postback(event)

            return HttpResponse(status=status.HTTP_200_OK)
        else:
            logger.info("Not an page Object : ")
