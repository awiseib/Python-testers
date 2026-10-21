from ibapi.tag_value import TagValue
from ibapi.client import *
from ibapi.wrapper import *



class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):

        mycontract = Contract()
        mycontract.symbol = "SHEL"
        mycontract.exchange = "SMART"
        mycontract.currency = "GBP"
        mycontract.primaryExchange = "LSE"
        mycontract.secType = "STK"
        
        myorder = Order()
        myorder.action = "BUY"
        myorder.orderType = "LMT"
        myorder.lmtPrice = 3814
        myorder.totalQuantity = 10000
        myorder.tif = "DAY"
        # myorder.postToAts=True
        myorder.algoStrategy = "Adaptive"
        myorder.algoParams = [
            TagValue("adaptivePriority", "Normal")
        ]
        # self.reqOpenOrders()
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
app.connect(host="127.0.0.1", port=7497, clientId=0)
app.run()
