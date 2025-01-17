from decimal import Decimal
from ibapi.client import *
from ibapi.common import OrderId
from ibapi.contract import Contract
from ibapi.order import Order
from ibapi.order_state import OrderState
from ibapi.wrapper import *
from ibapi.order_state import *
from datetime import datetime
from threading import Thread
import time

port = 7496


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)
        self.orderId = 0

    def nextValidId(self, orderId: OrderId):
        print(f"nextValidId. orderId={orderId}")
        self.orderId = orderId
    
    def nextOid(self):
        self.orderId += 1
        return self.orderId

    def openOrder(self, orderId: int, contract: Contract, order: Order, orderState: OrderState):
        print(f"openOrder. orderId: {orderId}, contract: {contract.symbol}, order: {order}, orderState: {orderState.status}")
    
    def orderStatus(self, orderId: OrderId, status: str, filled: Decimal, remaining: Decimal, avgFillPrice: float, permId: OrderId, parentId: OrderId, lastFillPrice: float, clientId: OrderId, whyHeld: str, mktCapPrice: float):
        print(f"orderStatus. OrderId: {orderId}, Status: {status}")


app = TestApp()
app.connect("127.0.0.1", port, 1001)
time.sleep(3)
Thread(target=app.run).start()
app.nextValidId(-1)
time.sleep(1)

### Leg for AAPL
leg1_contract = Contract() 
leg1_contract.conId = 265598
leg1_contract.exchange = "SMART"

leg1_order = Order()
leg1_order.tif = "DAY"
leg1_order.orderId = app.nextOid()
leg1_order.action = "BUY"
leg1_order.orderType = "LMT"
leg1_order.lmtPrice = 250
leg1_order.totalQuantity = 1
leg1_order.ocaGroup = "TestOCA_", leg1_order.orderId
leg1_order.ocaType = 1
leg1_order.transmit = True

app.placeOrder(leg1_order.orderId, leg1_contract, leg1_order)

## Leg for IBM
leg2_contract = Contract() 
leg2_contract.conId = 8314
leg2_contract.exchange = "SMART"

leg2_order = Order()
leg2_order.tif = "GTC"
leg2_order.orderId = app.nextOid()
leg2_order.action = "SELL"
leg2_order.orderType = "LMT"
leg2_order.lmtPrice = 229
leg2_order.totalQuantity = 1
leg2_order.ocaGroup = "TestOCA_", leg1_order.orderId
leg2_order.ocaType = 1
leg2_order.transmit = True

app.placeOrder(leg2_order.orderId, leg2_contract, leg2_order)

## Leg for KO
leg3_contract = Contract() 
leg3_contract.conId = 8894
leg3_contract.exchange = "SMART"

leg3_order = Order()
leg3_order.tif = "GTC"
leg3_order.orderId = app.nextOid()
leg3_order.action = "BUY"
leg3_order.orderType = "LMT"
leg3_order.totalQuantity = 62
leg3_order.lmtPrice = 10
leg3_order.ocaGroup = "TestOCA_", leg1_order.orderId
leg3_order.ocaType = 1
leg3_order.transmit = True

app.placeOrder(leg3_order.orderId, leg3_contract, leg3_order)
