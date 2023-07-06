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
        mycontract.symbol = "AAPL"
        mycontract.secType = "STK"
        mycontract.exchange = "SMART"
        mycontract.currency = "USD"


        myorder = Order()
        myorder.action = "BUY"
        myorder.totalQuantity = 100
        # myorder.lmtPrice = 288.00
        myorder.orderType = "MKT"
        myorder.tif = "DAY"
        myorder.goodAfterTime = "20230609 18:00:00 US/Eastern"
        # myorder.goodTillDate = "20230425 18:00:00 US/Eastern"
        # myorder.whatIf = True

        app.placeOrder(orderId, mycontract, myorder)

    def openOrder(self, orderId: OrderId, contract: Contract, order: Order, orderState: OrderState):
        print("openOrder.", orderId, contract, order)
        print(orderState.initMarginChange)

    def orderStatus(self, orderId: OrderId, status: str, filled: Decimal, remaining: Decimal, avgFillPrice: float, permId: int, parentId: int, lastFillPrice: float, clientId: int, whyHeld: str, mktCapPrice: float):
        print("orderStatus", "datetime: ",datetime.now(), orderId, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice)
    

app = TestApp()
app.connect("127.0.0.1", port, 0)
app.run()

