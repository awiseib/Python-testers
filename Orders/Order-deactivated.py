# Import our Sync Wrapper and Contract objects

from ibapi.sync_wrapper import *
from datetime import datetime
# Instantiate the reference for our sync class
app = TWSSyncWrapper(timeout=30)
# make a connection to Trader Workstation
# In this case, we're connecting on Localhost with port 7496 and Client ID 0.
# Connect to TWS
if not app.connect_and_start(host="127.0.0.1", port=7496, client_id=0):
    print("Failed to connect to TWS")
    exit(1)
else:
    print("Connected to TWS")
    

# app.reqOpenOrders()
# nid = app.get_next_valid_id()
# time_value = app.get_current_time()

# print(app.get_account_summary(AccountSummaryTags.AllTags, "All"))
'''
Create a contract class reference.
In our case, we'll be testing with AAPL.
TZA, APA, LABU, SOXS, UVXY, JDST, LRCX, BOIL
'''
contract = Contract()
contract.conId = 265598
contract.symbol = "AAPL"
contract.secType = "STK"
contract.exchange = "SMART"

# print(app.get_portfolio())
order = Order()
order.action = "BUY"
order.orderType = "LMT"
order.totalQuantity = 250
order.lmtPrice = 280
order.tif = "DAY"
order.deactivate = True
order_status = app.place_order_sync(contract, order)
oid = order_status["orderId"]
print(order_status)

app.disconnect_and_stop()
exit()