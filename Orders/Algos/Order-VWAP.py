from ibapi.tag_value import TagValue
from ibapi.client import *
from ibapi.wrapper import *

port = 7496


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        contract = Contract()
        contract.symbol = "F"
        contract.secType = "STK"
        contract.exchange = "SMART"
        contract.currency = "USD"
        
        order = Order()
        order.action = "BUY"
        order.totalQuantity = 1
        order.orderType = "LMT"
        order.lmtPrice = 9.81
        order.tif = "DAY"
        # order.outsideRth = True
        order.algoStrategy = "Vwap"

        order.algoParams = []
        order.algoParams.append(TagValue("maxPctVol", .3))
        order.algoParams.append(TagValue("startTime", "16:02:00 US/Los_Angeles"))
        order.algoParams.append(TagValue("endTime", "23:30:00 US/Los_Angeles"))
        order.algoParams.append(TagValue("allowPastEndTime",int(0)))
        order.algoParams.append(TagValue("noTakeLiq", int(0)))
        order.algoParams.append(TagValue("speedUp", int(1)))

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

