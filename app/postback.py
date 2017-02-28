import logic
from const import *


def received_postback(event):
    sender_id = event["sender"]["id"];
    postback = event['postback'];
    payload = postback['payload'];
    handle_payload(sender_id, payload);


def handle_payload(sender_id, payload):
    if payload.startswith(PAYLOAD_CATEGORY_QUICK_REPLY, 0):
        split_array = payload.split("_");
        print "Category" + split_array[0] + split_array[1]
        category_id = split_array[1]
        logic.handle_category_reply(sender_id, category_id);
    elif payload.startswith(PAYLOAD_GETTING_START_BUTTON_CLICK, 0):
        logic.handle_getting_start(sender_id);
