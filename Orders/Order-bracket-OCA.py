from ibapi.client import *
from ibapi.wrapper import *

import threading,time
port = 7496


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)
        self.oid = 0
        self.child_oid = 0
        self.oStatus = ""
        self.ptGroup = ""

    def nextValidId(self, orderId: OrderId):
        self.oid = orderId

    def nextOid(self):
        self.oid += 1
        return self.oid

    def openOrder(self, orderId: OrderId, contract: Contract, order: Order, orderState: OrderState):
        print(f"openOrder. orderId: {orderId}, contract: {contract}, order: {order}, orderState: {orderState.status}, submitter: {order.submitter}") 

    def orderStatus(self, orderId: TickerId, status: str, filled: Decimal, remaining: Decimal, avgFillPrice: float, permId: TickerId, parentId: TickerId, lastFillPrice: float, clientId: TickerId, whyHeld: str, mktCapPrice: float):
        print(orderId, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice)

    def error(self, reqId: TickerId, errorTime: int, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(f"Error., Time of Error: {errorTime}, Error Code: {errorCode}, Error Message: {errorString}")
        if advancedOrderRejectJson != "":
            print(f"AdvancedOrderRejectJson: {advancedOrderRejectJson}")
            
app = TestApp()
app.connect("127.0.0.1", 7496, 1001)
time.sleep(1)
threading.Thread(target=app.run).start()
time.sleep(1)
app.reqIds(-1)
time.sleep(1)

mycontract = Contract()
mycontract.conId = 265598
mycontract.exchange = "SMART"

parent_price = 238.90
quantity = 10.0

parent = Order()
parent.orderId = app.nextOid()
parent.action = "BUY"
parent.orderType = "LMT"
parent.totalQuantity = quantity
# parent.outsideRth = True
parent.lmtPrice = parent_price
parent.transmit = False
app.placeOrder(parent.orderId, mycontract, parent)
time.sleep(1)
profit_taker = Order()
profit_taker.orderId = parent.orderId + 1
profit_taker.parentId = parent.orderId
profit_taker.action = "SELL"
profit_taker.orderType = "LMT"
profit_taker.totalQuantity = quantity
profit_taker.lmtPrice = parent_price + 10
# profit_taker.ocaGroup = f"OCA_{profit_taker.orderId}"
profit_taker.transmit = True

app.child_oid = profit_taker.orderId

app.placeOrder(profit_taker.orderId, mycontract, profit_taker)
##### 
while app.oStatus != "Submitted":
    time.sleep(0.1)

oca_addon = Order()
oca_addon.orderId = app.child_oid + 1
# oca_addon.parentId = parent.orderId
oca_addon.action = "SELL"
oca_addon.orderType = "LMT"
oca_addon.totalQuantity = quantity
oca_addon.lmtPrice = parent_price + 15
oca_addon.ocaGroup = app.ptGroup
oca_addon.transmit = True

app.placeOrder(oca_addon.orderId, mycontract, oca_addon)