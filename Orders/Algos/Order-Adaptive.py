from ibapi.client import *
from ibapi.order_state import OrderState
from ibapi.wrapper import *
from ibapi.tag_value import TagValue

port = 7496


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):

        mycontract = Contract()
        mycontract.symbol = "XLC"
        mycontract.secType = "STK"
        mycontract.currency = "USD"
        mycontract.exchange = "SMART"
        
        myorder = Order()
        myorder.action = "BUY"
        myorder.orderType = "LMT"
        myorder.lmtPrice = 100
        myorder.totalQuantity = 26
        
        myorder.algoStrategy = "Adaptive"
        myorder.algoParams = [
            TagValue("adaptivePriority", "Normal")
        ]

        self.placeOrder(orderId, mycontract, myorder)

    def openOrder(self, orderId: int, contract: Contract, order: Order, orderState: OrderState):
        print(orderId, contract, order, orderState)

    def error(self, reqId: TickerId, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print("ERROR: ",errorCode, errorString)


app = TestApp()
app.connect("127.0.0.1", port, 1001)
app.run()
