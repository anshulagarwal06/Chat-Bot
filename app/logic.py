import accounts.models as account_models
import store.models as store_models
import fbcalls
from const import *


def handle_category_reply(sender_id, category_id):
    # get customers
    customer = account_models.fetch_customers_details(sender_id)

    store = store_models.get_customers_store(customer);
    store_product = store_models.StoreProducts.objects.filter(store=store, product__Category__id=category_id);

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
