from ibapi.client import *
from ibapi.wrapper import *
from ibapi.tag_value import TagValue

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
        myorder.lmtPrice = 95
        myorder.totalQuantity = 50
        myorder.tif = "DAY"
        myorder.algoStrategy = "ArrivalPx"
        myorder.algoParams = []
        myorder.algoParams.append(TagValue("maxPctVol", 0.1))
        myorder.algoParams.append(TagValue("riskAversion", "Aggressive"))
        myorder.algoParams.append(TagValue("startTime", "20240703-16:00:00"))
        myorder.algoParams.append(TagValue("endTime", "20240703-17:00:00"))
        myorder.algoParams.append(TagValue("allowPastEndTime",1))
        myorder.algoParams.append(TagValue("forceCompletion",0))

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
