import json
import requests


def sentTextMessage(recipientId, messageText=None, quick_replies=None, attachment=None):
    data = {}
    recipient = {};

    recipient['id'] = recipientId;

    message = {}
    if messageText:
        message['text'] = messageText;
    if quick_replies:
        message['quick_replies'] = json.dumps(quick_replies)
    if attachment:
        message['attachment'] = attachment;

    data['message'] = message
    data['recipient'] = recipient;

    print json.dumps(data)
    # json_data = json.dumps(data)
    callSentAPI(data)


def callSentAPI(data):
    url = 'https://graph.facebook.com/v2.8/me/messages'
    url = url + "?" + "access_token=EAAWS4fk3smoBAIyUdqQbKZCjICHwr2ZAkVhM8oDOyppnZBoJLNeQ5IjeAUrlf5X3jYV0rxvZCs0eZABSH79eCpUBHeosZBPiB3QUYrYAP7kmgwfCS6DfTQZASj05RgmFRcdjSfXaVrpnZChcvQEUH1ZBY9GFCZAJb1g87ie4uBQcNQ1QZDZD"
    request = requests.post(url, json=data);

    print request.url;
    print request.status_code;
    print request.text
