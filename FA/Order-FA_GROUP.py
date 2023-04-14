from ibapi.client import *
from ibapi.wrapper import *

from datetime import datetime

port = 7496


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):

        mycontract = Contract()
        mycontract.symbol = "AMD"
        mycontract.secType = "STK"
        mycontract.exchange = "SMART"
        mycontract.currency = "USD"

        myorder = Order()
        myorder.action = "BUY"
        myorder.totalQuantity = 11
        myorder.orderType = "MKT"

        myorder.faGroup = "Test_2"
        myorder.faMethod = "EqualQuantity"

        self.placeOrder(orderId, mycontract, myorder)

    def openOrder(self, orderId: OrderId, contract: Contract, order: Order, orderState: OrderState):
        print("openOrder",  "datetime: ",datetime.now(), orderState.status)

    def orderStatus(self, orderId: OrderId, status: str, filled: Decimal, remaining: Decimal, avgFillPrice: float, permId: int, parentId: int, lastFillPrice: float, clientId: int, whyHeld: str, mktCapPrice: float):
        print("orderStatus", "datetime: ",datetime.now(), orderId, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice)

    def execDetails(self, reqId: int, contract: Contract, execution: Execution):
        print(f"execDetails. contract: {contract},  execution: {execution}")
    

app = TestApp()
app.connect("127.0.0.1", port, 0)
app.run()

