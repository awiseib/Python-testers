# Import our Sync Wrapper and Contract objects

from ibapi.sync_wrapper import *
from datetime import datetime
# Instantiate the reference for our sync class
app = TWSSyncWrapper(timeout=30)
# make a connection to Trader Workstation
# In this case, we're connecting on Localhost with port 7496 and Client ID 0.
# Connect to TWS
if not app.connect_and_start(host="127.0.0.1", port=7496, client_id=8675309):
    print("Failed to connect to TWS")
    exit(1)
else:
    print("Connected to TWS")
    

app.reqOpenOrders()
nid = app.get_next_valid_id()
time_value = app.get_current_time()

print(app.get_account_summary(AccountSummaryTags.AllTags, "All"))
'''
Create a contract class reference.
In our case, we'll be testing with AAPL.
TZA, APA, LABU, SOXS, UVXY, JDST, LRCX, BOIL
'''
contract = Contract()
contract.conId = 265598
# contract.symbol = "SPY"
contract.secType = "STK"
contract.exchange = "SMART"
# contract.primaryExchange = "ISLAND"
contract.currency = "USD"

# '''
# Contract details requests will return all contracts the match the details
# of our contract object in a list. Because a list is returned, we are 
# taking the first (or 0 index) contract returned. 
# # '''
print(app.get_contract_details(contract))
aapl_contract = app.get_contract_details(contract)[0].contract
# app.reqMarketDataType(3)
market_data = app.get_market_data_snapshot(aapl_contract)
market_data = app.get_market_data_snapshot(aapl_contract, generic_tick_list="165,225,293,294,295,233,375", snapshot=False)

print(market_data)
print(market_data["LAST_TIMESTAMP"])

bars = app.get_historical_data(
        contract=contract,
        end_date_time="", # Empty for current time
        duration_str="5 Y",
        bar_size_setting="1 day",
        what_to_show="TRADES",
        use_rth=True
        )

for bar in bars: print(bar)

print(app.get_portfolio())
order = Order()
order.action = "BUY"
order.orderType = "LMT"
order.totalQuantity = 100
order.lmtPrice = 240 # market_data["price"][1]["price"]
order.tif = "GTC"
# # # order.transmit = False
# order.outsideRth = True
order_status = app.place_order_sync(contract, order)
oid = order_status["orderId"]
print(order_status)
open_orders = app.get_open_orders()
newO = open_orders[oid]['order']
newC = open_orders[oid]['contract']
newO.lmtPrice = 260
app.placeOrder(newO.orderId, newC, newO)

print(app.cancel_order_sync(oid, OrderCancel()))

print(app.get_executions(ExecutionFilter()))
positions = app.get_positions()["DU5240685"]
for pos in positions:
    if pos["contract"].conId == 265598:
        print(pos)

print(app.get_portfolio("DU5240685"))

app.disconnect_and_stop()
exit()