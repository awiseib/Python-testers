from ibapi.client import *
from ibapi.wrapper import *
from ibapi.tag_value import TagValue


port = 7496

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):

        mycontract = Contract()
        # mycontract.symbol = "AAPL"
        # mycontract.secType = "STK"
        # mycontract.currency = "USD"
        mycontract.conId = 533620665
        mycontract.exchange = "QBALGO"
        # mycontract.primaryExchange = "ISLAND"
        
        baseOrder = Order()
        baseOrder.action = "BUY"
        baseOrder.totalQuantity = 10
        baseOrder.orderType = "MKT"
        # baseOrder.lmtPrice = 180
        baseOrder.outsideRth = True

        baseOrder.algoStrategy = "Octane"
        baseOrder.algoParams = []
        baseOrder.algoParams.append(TagValue("StartTime", "13:00:00 America/Chicago"))
        baseOrder.algoParams.append(TagValue("EndTime", "15:00:00 America/Chicago"))
        baseOrder.algoParams.append(TagValue("Duration", "-99"))
        baseOrder.algoParams.append(TagValue("Urgency", "High"))

        self.placeOrder(orderId, mycontract, baseOrder)


    def openOrder(self, orderId: OrderId, contract: Contract, order: Order, orderState: OrderState):
        print(orderId, contract, order, orderState)
    
    def orderStatus(self, orderId: OrderId, status: str, filled: Decimal, remaining: Decimal, avgFillPrice: float, permId: int, parentId: int, lastFillPrice: float, clientId: int, whyHeld: str, mktCapPrice: float):
        print(orderId, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice)
    
    def error(self, reqId: TickerId, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(reqId, errorCode, errorString, advancedOrderRejectJson)


app = TestApp()
app.connect("127.0.0.1", port, 1001)
app.run()
