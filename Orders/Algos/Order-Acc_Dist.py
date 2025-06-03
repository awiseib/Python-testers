from ibapi.tag_value import TagValue
from ibapi.client import *
from ibapi.wrapper import *
from ibapi.contract import ComboLeg

port = 7496


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):

        mycontract = Contract()
        mycontract.symbol = "AAPL"
        mycontract.secType = "STK"
        mycontract.currency = "USD"
        mycontract.exchange = "SMART"

        
        myorder = Order()
        myorder.action = "BUY"
        myorder.orderType = "MKT"
        # myorder.lmtPrice = 190
        myorder.totalQuantity = 2
        # myorder.outsideRth = True
        myorder.algoStrategy = "AccuDistr"
        myorder.algoParams = []
        myorder.algoParams.append(TagValue("componentSize", 5))
        myorder.algoParams.append(TagValue("timeBetweenOrders", 30))
        myorder.algoParams.append(TagValue("randomizeTime20", 0))
        myorder.algoParams.append(TagValue("randomizeSize55", 0))
        myorder.algoParams.append(TagValue("routeOrderType", "MKT"))
        # myorder.algoParams.append(TagValue("routePercentOffset", 0.0025))
        # myorder.algoParams.append(TagValue("routeOffset", 1.25))
        myorder.algoParams.append(TagValue("catchUp", 1))
        myorder.algoParams.append(TagValue("waitForFill", 1))
        myorder.algoParams.append(TagValue("activeTimeStart", "09:30:00 US/Eastern"))
        myorder.algoParams.append(TagValue("activeTimeEnd", "10:20:00 US/Eastern"))

        self.placeOrder(orderId, mycontract, myorder)

    def openOrder(self, orderId: OrderId, contract: Contract, order: Order, orderState: OrderState):
        print(f"openOrder. orderId: {orderId}, contract: {contract}, order: {order}, Algo Details: {order.algoParams}") 

    def orderStatus(self, orderId: TickerId, status: str, filled: Decimal, remaining: Decimal, avgFillPrice: float, permId: TickerId, parentId: TickerId, lastFillPrice: float, clientId: TickerId, whyHeld: str, mktCapPrice: float):
        print(orderId, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice)

    def error(self, reqId: TickerId, errorTime: int, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(f"Error., Time of Error: {errorTime}, Error Code: {errorCode}, Error Message: {errorString}")
        if advancedOrderRejectJson != "":
            print(f"AdvancedOrderRejectJson: {advancedOrderRejectJson}")
            
app = TestApp()
app.connect("127.0.0.1", port, 0)
app.run()
