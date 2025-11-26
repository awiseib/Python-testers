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
        myorder.orderId=1784380540
        myorder.action = "BUY"
        myorder.orderType = "LMT"
        myorder.lmtPrice = 215
        myorder.totalQuantity = 1
        myorder.tif = "GTC"
        myorder.postToAts=True
        myorder.algoStrategy = "Adaptive"
        myorder.algoParams = [
            TagValue("adaptivePriority", "Normal")
        ]
        self.reqOpenOrders()
        # self.placeOrder(1784380540, mycontract, myorder)

    def openOrder(self, orderId: OrderId, contract: Contract, order: Order, orderState: OrderState):
        print(f"openOrder. orderId: {orderId}, contract: {contract}, order: {order}, orderState: {orderState.status}, submitter: {order.submitter}") 
        if orderId == 1784380537 and order.lmtPrice == 212:
            order.lmtPrice = 215
            # order.postToAts = True
            self.placeOrder(1784380537, contract, order)

    def orderStatus(self, orderId: TickerId, status: str, filled: Decimal, remaining: Decimal, avgFillPrice: float, permId: TickerId, parentId: TickerId, lastFillPrice: float, clientId: TickerId, whyHeld: str, mktCapPrice: float):
        print(orderId, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice)

    def error(self, reqId: TickerId, errorTime: int, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(f"Error., Time of Error: {errorTime}, Error Code: {errorCode}, Error Message: {errorString}")
        if advancedOrderRejectJson != "":
            print(f"AdvancedOrderRejectJson: {advancedOrderRejectJson}")
            
app = TestApp()
app.connect("127.0.0.1", port, 0)
app.run()
