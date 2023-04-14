from ibapi.client import *
from ibapi.wrapper import *
import time
from datetime import datetime

port = 7496


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: int):
        mycontract = Contract()
        mycontract.symbol = "KMI"
        mycontract.secType = "STK"
        mycontract.exchange = "SMART"
        mycontract.currency = "USD"


        myorder = Order()
        myorder.account
        myorder.action = "BUY"
        myorder.totalQuantity = 5713
        # myorder.lmtPrice = 138.00
        myorder.orderType = "MKT"
        myorder.tif = "DAY"

        app.placeOrder(orderId, mycontract, myorder)

    def openOrder(self, orderId: OrderId, contract: Contract, order: Order, orderState: OrderState):
        print("openOrder.", orderId, contract, order)

    def orderStatus(self, orderId: OrderId, status: str, filled: Decimal, remaining: Decimal, avgFillPrice: float, permId: int, parentId: int, lastFillPrice: float, clientId: int, whyHeld: str, mktCapPrice: float):
        print("orderStatus", orderId, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice)
    

app = TestApp()
app.connect("127.0.0.1", port, 1000)
app.run()

