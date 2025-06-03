from ibapi.client import *
from ibapi.wrapper import *
from ibapi.tag_value import TagValue

port = 7496

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):

        mycontract = Contract()
        mycontract.conId = 554291368
        mycontract.exchange = "NYBOT" 
        
        baseOrder = Order()
        baseOrder.action = "BUY"
        baseOrder.totalQuantity = 7
        baseOrder.orderType = "MKT"
        baseOrder.tif = "GTC"
        # baseOrder.outsideRth = True

        baseOrder.algoStrategy = "AD"
        baseOrder.algoParams = []
        baseOrder.algoParams.append(TagValue("componentSize", 1))
        baseOrder.algoParams.append(TagValue("timeBetweenOrders", 60))
        baseOrder.algoParams.append(TagValue("randomizeTime20", int(1)))
        baseOrder.algoParams.append(TagValue("randomizeSize55", int(1)))
        baseOrder.algoParams.append(TagValue("giveUp", ''))
        baseOrder.algoParams.append(TagValue("catchUp", int(0)))
        baseOrder.algoParams.append(TagValue("waitForFill", int(0)))
        baseOrder.algoParams.append(TagValue("activeTimeStart", "17:05:00 US/Eastern"))
        baseOrder.algoParams.append(TagValue("activeTimeEnd", "17:07:00 US/Eastern"))

        self.placeOrder(orderId, mycontract, baseOrder)

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
