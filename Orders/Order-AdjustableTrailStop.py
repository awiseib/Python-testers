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

        # Adjusted trail limit
        order2 = Order()
        order2.parentId = order1.orderId
        order2.orderId = orderId+1
        order2.action = "BUY"
        order2.tif = "DAY"
        order2.totalQuantity = 10
        
        order2.triggerPrice = 175
        order2.adjustedOrderType = "TRAIL LIMIT"
        order2.adjustedStopPrice = 173
        order2.lmtPriceOffset = 1
        order2.auxPrice = 3

        self.placeOrder(order1.orderId, mycontract, order1)
        self.placeOrder(order2.orderId, mycontract, order2)


    def openOrder(self, orderId: OrderId, contract: Contract, order: Order, orderState: OrderState):
        print(f"openOrder. orderId: {orderId}, contract: {contract}, order: {order}") 
        print(f"Maintenance Margin: {orderState.maintMarginAfter}, {orderState.maintMarginBefore}, {orderState.maintMarginChange}")
        print(f"Initial Margin: {orderState.initMarginAfter}, {orderState.initMarginBefore}, {orderState.initMarginChange}")


    def orderStatus(self, orderId: OrderId, status: str, filled: Decimal, remaining: Decimal, avgFillPrice: float, permId: int, parentId: int, lastFillPrice: float, clientId: int, whyHeld: str, mktCapPrice: float):
        print(f"orderId: {orderId}, status: {status}, filled: {filled}, remaining: {remaining}, avgFillPrice: {avgFillPrice}, permId: {permId}, parentId: {parentId}, lastFillPrice: {lastFillPrice}, clientId: {clientId}, whyHeld: {whyHeld}, mktCapPrice: {mktCapPrice}")

    def error(self, reqId: TickerId, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(reqId, errorCode, errorString, advancedOrderRejectJson)

app = TestApp()
app.connect("127.0.0.1", port, 7496)
app.run()