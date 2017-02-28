from const import *
import fbcalls


def is_ignore_qr(sender_id, message, quick_reply):
    if quick_reply['payload']:
        payload = quick_reply['payload'];
        if payload == PAYLOAD_QUICK_REPLY_IGNORE:
            fbcalls.sentTextMessage(sender_id, "Mmm.")
            return True
    return False;


def get_quick_reply_object(type):
    reply = {}
    if type == TYPE_QUICK_REPLY_LOCATION:
        reply['content_type'] = 'location'
        return reply
    elif type == TYPE_QUICK_REPLY_IGNORE:
        reply['content_type'] = 'text'
        reply['title'] = 'Never mind'
        reply['payload'] = PAYLOAD_QUICK_REPLY_IGNORE;
        return reply
