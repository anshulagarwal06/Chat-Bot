import accounts
import accounts.models as account_models
import store.models as store_models
import cart.models as cart_models
from cart.models import StoreProducts
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
        reply['payload'] = PAYLOAD_PRODUCT_QUICK_REPLY + str(product_object.id)
        quick_replies.append(reply)
        message = message + product_object.product.product_name + '\n'

    fbcalls.sentTextMessage(sender_id, message, quick_replies=quick_replies);


def add_product_to_cart(sender_id, product_id, quantity=1):
    # get product object
    store_product = store_models.StoreProducts.objects.get(id=product_id);

    # get user from sender_id:
    customer = accounts.models.fetch_customers_details(sender_id);

    # get user cart
    # delete check will be added later
    cart = cart_models.get_user_cart(customer=customer)

    # create cart line item
    cart_models.add_product_to_cartline(cart, store_product, quantity)

    message = "Successfully added to your cart.\n\nType \"Cart\" to see your cart."

    fbcalls.sentTextMessage(sender_id, message);


def show_user_cart(sender_id):
    # get customer object
    customer = accounts.models.fetch_customers_details(sender_id)

    # get customer cart
    cart = cart_models.get_user_cart(customer);

    # get all cart items
    cart_lines = cart_models.get_cart_line_items(cart)

    message = " Cart details -" + '\n\n'
    count = 1;
    total_price = 0
    for items in cart_lines:
        store_product = StoreProducts.objects.get(id=items.store_product.id);
        product = store_product.product
        name = product.product_name;
        item_price = store_product.price;
        quantity = items.quantity;
        price = item_price * quantity

        message = message + str(count) + ". " + name + "\t\t" + str(quantity) + "*" + str(item_price) + '\t\t' + str(
            int(price)) + "\n\n"

        total_price = total_price + price;
        count += 1

    message = message + "Total" + '\t\t\t' + str(total_price)
    fbcalls.sentTextMessage(sender_id, message);
