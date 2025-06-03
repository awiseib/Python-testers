from ibapi.client import *
from ibapi.wrapper import *

port=7496

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):

        mycontract = Contract()
        mycontract.symbol = "AAPL"
        mycontract.secType = "STK"    
        mycontract.exchange = "SMART"
        mycontract.currency = "USD"

        # Standard LMT
        order1 = Order()
        order1.orderId = orderId
        order1.action = "BUY"
        order1.tif = "DAY"
        order1.totalQuantity = 10
        order1.orderType = "MKT"
        order1.transmit = False

        # Adjusted trail limit
        order2 = Order()
        # order2.parentId = order1.orderId
        order2.orderId = orderId+1
        order2.action = "SELL"
        order2.tif = "DAY"
        order2.totalQuantity = 10
        order2.orderType = "STP"
        order2.triggerPrice = 175
        order2.adjustedOrderType = "TRAILLIMIT"
        order2.adjustedStopPrice = 173
        order2.adjustedTrailingAmount = 205
        order2.adjustedStopLimitPrice = 200
        order2.lmtPriceOffset = 1
        order2.auxPrice = 3
        order2.transmit = False

        # self.placeOrder(order1.orderId, mycontract, order1)
        self.placeOrder(order2.orderId, mycontract, order2)

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