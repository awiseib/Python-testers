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
c1.conId = 265598
c1.exchange = "SMART"

### Leg for IBM
c2 = Contract() 
c2.conId = 8314
c2.exchange = "SMART"

o1 = Order()
o1.tif = "GTC"
o1.orderId = app.nextOid()
o1.action = "BUY"
o1.orderType = "MKT"
o1.totalQuantity = 1
o1.ocaGroup = f"TestOCA_{o1.orderId}"
o1.ocaType = 3

o2 = Order()
o2.tif = "GTC"
o2.orderId = app.nextOid()
o2.permId = app.permId
o2.action = "BUY"
o2.orderType = "MKT"
o2.totalQuantity = 1
o2.ocaGroup = f"TestOCA_{o1.orderId}"


app.placeOrder(o1.orderId, c1, o1)
app.placeOrder(o2.orderId, c2, o2)