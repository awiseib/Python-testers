from ibapi.tag_value import TagValue
from ibapi.client import *
from ibapi.wrapper import *

port = 7496


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):

        mycontract = Contract()
        mycontract.conId = 265598
        mycontract.exchange = "SMART"
        
        myorder = Order()
        myorder.action = "BUY"
        myorder.orderType = "LMT"
        myorder.lmtPrice = 187
        myorder.totalQuantity = 50
        
        myorder.algoStrategy = "PctVol"
        myorder.algoParams = []
        myorder.algoParams.append(TagValue("pctVol", "0.5"))
        myorder.algoParams.append(TagValue("startTime", "15:00:00 US/Eastern"))
        myorder.algoParams.append(TagValue("endTime", "17:00:00 US/Eastern"))
        myorder.algoParams.append(TagValue("noTakeLiq", "1"))

        self.placeOrder(orderId, mycontract, myorder)

    def openOrder(self, orderId: OrderId, contract: Contract, order: Order, orderState: OrderState):
        print(f"openOrder. orderId: {orderId}, contract: {contract}, order: {order}, orderState: {orderState.status}, submitter: {order.submitter}") 

    def orderStatus(self, orderId: TickerId, status: str, filled: Decimal, remaining: Decimal, avgFillPrice: float, permId: TickerId, parentId: TickerId, lastFillPrice: float, clientId: TickerId, whyHeld: str, mktCapPrice: float):
        print(orderId, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice)

    def error(self, reqId: TickerId, errorTime: int, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(f"Error., Time of Error: {errorTime}, Error Code: {errorCode}, Error Message: {errorString}")
        if advancedOrderRejectJson != "":
            print(f"AdvancedOrderRejectJson: {advancedOrderRejectJson}")
            
app = TestApp()
app.connect("127.0.0.1", port, 0)
app.run()
