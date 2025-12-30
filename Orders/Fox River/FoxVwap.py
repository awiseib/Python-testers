# Import our Sync Wrapper and Contract objects

from ibapi.tag_value import TagValue
from ibapi.sync_wrapper import *
app = TWSSyncWrapper(timeout=30)
if not app.connect_and_start(host="127.0.0.1", port=7496, client_id=8675309):
    print("Failed to connect to TWS")
    exit(1)
else:
    print("Connected to TWS")


contract = Contract()
contract.conId = 265598
contract.exchange = "FOXRIVER"

order = Order()
order.action = "BUY"
order.orderType = "LMT"
order.lmtPrice = 265
order.totalQuantity = 100
order.tif = "DAY"
order.transmit = False

order.algoStrategy = "FoxVWAP"
order.algoParams = [
    TagValue("EffectiveTime", "15:00:00 US/Eastern"),
    TagValue("ExpireTime", "15:45:00 US/Eastern"),
    TagValue("PartRateLimit", 0.05),
    TagValue("EndTimeBehavior", "Hard_EndTime"), # Hard_EndTime, Cancel_balance, or an empty string.
    TagValue("Elasticity", "Medium"), # Low, Medium, High
    TagValue("DarkAttack", "10-Most_aggressive"), # 0-Do_not_favor_dark_pools, 1-Least_aggressive, 2,3,4,5,6,7,8,9, 10-Most_aggressive
    TagValue("IWouldDark", 0),
    TagValue("SweepPrice", 304),
    TagValue("DollarCertainLimit", 260),
    TagValue("DollarCertainCommission", 10),
    TagValue("DollarCertainExecution", 1),
    TagValue("CorpBuyBack", 1)
]

app.place_order_sync(contract,order)


app.disconnect_and_stop()
exit()