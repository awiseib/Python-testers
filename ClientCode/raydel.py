from decimal import Decimal
from ibapi.client import *
from ibapi.wrapper import *
from datetime import datetime
from ibapi.contract import *
from ibapi.order_state import *

port = 7496


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        print(f"nextValidId. orderId={orderId}")

        parentContract = Contract() 
        parentContract.conId = 7089 # FCX STK
        parentContract.exchange = "SMART"
        parentContract.currency = "USD"

        parentOrder = Order()
        parentOrder.orderId = orderId
        parentOrder.action = "BUY"
        parentOrder.orderType = "STP LMT"
        parentOrder.lmtPrice = 42.07
        parentOrder.auxPrice = 42.07
        parentOrder.totalQuantity = 10
        parentOrder.ocaGroup = "RAYDEL_OCA_", orderId
        parentOrder.ocaType = 1
        parentOrder.transmit = True

        self.placeOrder(orderId, parentContract, parentOrder)

        chilldO1 = Order()
        chilldO1.orderId = orderId + 1
        chilldO1.action = "SELL"
        chilldO1.orderType = "LMT"
        chilldO1.lmtPrice = 45.5
        chilldO1.totalQuantity = 10
        chilldO1.ocaGroup = "RAYDEL_OCA_", orderId
        chilldO1.ocaType = 1
        chilldO1.transmit = True

        self.placeOrder(chilldO1.orderId, parentContract, chilldO1)


    def openOrder(self, orderId: OrderId, contract: Contract, order: Order, orderState: OrderState):
        print("openOrder.", orderId, contract, order, orderState)

    def orderStatus(self, orderId: OrderId, status: str, filled: Decimal, remaining: Decimal, avgFillPrice: float, permId: int, parentId: int, lastFillPrice: float, clientId: int, whyHeld: str, mktCapPrice: float):
        print(f"orderStatus., orderId:{orderId}, status:{status}, filled:{filled}, remaining:{remaining}, avgFillPrice:{avgFillPrice}, parentId:{parentId}, lastFillPrice:{lastFillPrice}")

    def error(self, reqId: TickerId, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(reqId, errorCode, errorString, advancedOrderRejectJson)



app = TestApp()
app.connect("127.0.0.1", port, 1001)
app.run()
