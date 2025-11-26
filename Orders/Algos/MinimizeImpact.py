from ibapi.tag_value import TagValue
from ibapi.client import *
from ibapi.wrapper import *

port = 7496


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        contract = Contract()
        contract.conId = 785025858
        # contract.symbol = "KO"
        # contract.secType = "STK"
        contract.exchange = "SMART"
        contract.currency = "USD"
        
        order = Order()
        order.action = "BUY"
        order.totalQuantity = 100
        order.orderType = "LMT"
        order.lmtPrice = 25.5
        order.tif = "DAY"
        order.algoStrategy = "MinImpact"

        order.algoParams = []
        # order.algoParams.append(TagValue("componentSize", 100))
        # order.algoParams.append(TagValue("timeBetweenOrders", 1))
        # order.algoParams.append(TagValue("randomizeTime20", int(1)))
        # order.algoParams.append(TagValue("randomizeSize55", int(1)))
        # order.algoParams.append(TagValue("giveUp", 0))
        # order.algoParams.append(TagValue("catchUp", int(1)))
        # order.algoParams.append(TagValue("waitForFill", int(0)))
    
        self.placeOrder(orderId, contract, order)

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

