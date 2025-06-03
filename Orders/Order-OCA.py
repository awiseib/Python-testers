from ibapi.client import *
from ibapi.wrapper import *
from time import sleep
from threading import Thread

port = 7496


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)
        self.orderId = 0
        self.permId = 0

    def nextValidId(self, orderId: OrderId):
        self.orderId = orderId - 1

    def nextOid(self):
        self.orderId +=1
        return self.orderId

    def openOrder(self, orderId: OrderId, contract: Contract, order: Order, orderState: OrderState):
        print(f"openOrder. orderId: {orderId}, contract: {contract}, order: {order}, orderState: {orderState.status}, submitter: {order.submitter}")
        print(f"{orderId} for {contract.symbol} permId: {order.permId}")
        if orderId == app.orderId:
            self.permId = order.permId

    def orderStatus(self, orderId: TickerId, status: str, filled: Decimal, remaining: Decimal, avgFillPrice: float, permId: TickerId, parentId: TickerId, lastFillPrice: float, clientId: TickerId, whyHeld: str, mktCapPrice: float):
        print(orderId, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice)

    def error(self, reqId: TickerId, errorTime: int, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(f"Error., Time of Error: {errorTime}, Error Code: {errorCode}, Error Message: {errorString}")
        if advancedOrderRejectJson != "":
            print(f"AdvancedOrderRejectJson: {advancedOrderRejectJson}")
            
app = TestApp()
app.connect("127.0.0.1", port, 100)
sleep(3)
Thread(target=app.run).start()
sleep(1)


### Leg for AAPL
c1 = Contract() 
c1.conId = 766510430
c1.exchange = "SMART"

### Leg for AAPL
c2 = Contract() 
c2.conId = 766510798
c2.exchange = "SMART"

o1 = Order()
o1.tif = "GTC"
o1.orderId = app.nextOid()
o1.action = "BUY"
o1.orderType = "LMT"
o1.lmtPrice = 1.7
o1.totalQuantity = 1
o1.ocaGroup = "TestOCA_", o1.orderId
o1.ocaType = 3

o2 = Order()
o2.tif = "GTC"
o2.orderId = app.nextOid()
o2.permId = app.permId
o2.action = "BUY"
o2.orderType = "LMT"
o2.lmtPrice = 25.4
o2.totalQuantity = 1
o2.ocaGroup = "TestOCA_", o1.orderId
# o2.ocaType = 1

app.placeOrder(o1.orderId, c1, o1)
app.placeOrder(o2.orderId, c2, o2)

# app2 = TestApp()
# app2.connect("127.0.0.1", port, 0)
# sleep(3)
# Thread(target=app2.run).start()
# sleep(1)

# while True:
#     if app.permId != 0:
#         o2.lmtPrice = 215
#         app.placeOrder(o2.orderId, c2, o2)
#     sleep(3)
