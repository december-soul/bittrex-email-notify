from bittrex.bittrex import Bittrex
from time import time, sleep
from secret import BITTREX_KEY, BITTREX_SECRET, EMAIL_HOST, EMAIL_USER, EMAIL_PASS, EMAIL_FROM, EMAIL_TO
import smtplib


def sendemail( msgsub, msg_body ):
	server = smtplib.SMTP(EMAIL_HOST, 587)
	server.starttls()
	server.login(EMAIL_USER, EMAIL_PASS)
	
	msg_sub = 'Subject: Bittrex Mail Notification: ' + msgsub + '\r\n'
	msg_header = ("From: %s\r\nTo: %s\r\n\r\n" % (EMAIL_FROM, EMAIL_TO))
	msg = msg_sub + msg_header + msg_body
	
	server.sendmail(EMAIL_FROM, EMAIL_TO, msg)
	server.quit()


def ordertostring( order ):
	str = ''
	str += 'Exchange: ' + order['Exchange'] + '\r\n'
	str += 'OrderType: ' + order['OrderType'] + '\r\n'
	str += 'Limit: ' + "%.10f" % order['Limit'] + '\r\n'
	str += 'QuantityRemaining: ' + "%.10f" % order['QuantityRemaining'] + '\r\n'
	str += 'Quantity: ' + "%.10f" % order['Quantity'] + '\r\n'
	str += 'Price: ' + "%.10f" % order['Price'] + '\r\n'
	str += 'Opened: ' + order['Opened'] + '\r\n'
	str += '\r\n'
	#str += str(order)
	return str

LOOP_SLEEP_TIME = 15

#pb = PushBullet(api_key=PUSHBULLET_API)
exchange = Bittrex(
    BITTREX_KEY,
    BITTREX_SECRET
)
first_run = True
orders_present = {}

sendemail("start observer", "the Bittrex Mail Notification observer has been started")
while True:
    loop_start_time = time()
    orders_to_notify = []

    try:
        orders_current = exchange.get_open_orders()['result']
    except:
        print("catch exception from read orders\n")
	continue

    if first_run:
        for order in orders_current:
            orders_present[order['OrderUuid']] = order
        first_run = False
        continue

    try:
    # Build list of uuids present in orders
        order_uuids = [order['OrderUuid'] for order in orders_current]
    except:
        print("catch exception while parse orders")
        continue

    # Check if all uuids in orders_present are present in orders
    for uuid in orders_present.keys():
        if uuid in order_uuids:
            continue
        else:
            # Order is gone!
            orders_to_notify.append(orders_present[uuid])

    if len(orders_to_notify) > 0:
        # Push to pushbullet here
        print('Order disappeared! Canceled or sold!')
        note_to_push = ''
        for to_notify in orders_to_notify:
            ex = to_notify['Exchange']
            order_type = to_notify['OrderType']
            limit = to_notify['Limit']
            note_to_push += '%s : %s : %s' % (ex, order_type, limit)
#            note_to_push += '\n'
        print(note_to_push)
        sendemail(note_to_push, ordertostring(to_notify))

    # Reset orders_present to the current list
    orders_present = {order['OrderUuid']: order for order in orders_current}
    print('Orders present: %s' % orders_present)

    # Sleep for remaining time
    loop_end_time = time()
    remaining_time = LOOP_SLEEP_TIME - (loop_end_time - loop_start_time)
    sleep(max(0, remaining_time))

