from ibapi.client import *
from ibapi.wrapper import *

port=7497

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):

        contract = Contract()
        contract.symbol = "AAPL"
        contract.secType = "STK"    
        contract.exchange = "SMART"
        contract.currency = "USD"

        # Standard LMT
        order = Order()
        order.orderId = orderId
        order.action = "BUY"
        order.tif = "DAY"
        order.totalQuantity = 1000
        order.orderType = "STP"
        order.auxPrice = 297.14
        # order.trailStopPrice = 297.14 
        # order.trailingPercent = 3
        
        order.triggerPrice = 294.85
        order.adjustedOrderType = "TRAIL"
        order.adjustedStopPrice = 294.50
        order.adjustedTrailingAmount = 294.40
        order.adjustedStopLimitPrice = 294.75
        # order.lmtPriceOffset = 1
        # order.auxPrice = 3

        order.account = "DU74649"
        
        self.placeOrder(order.orderId, contract, order)

    def openOrder(self, orderId: OrderId, contract: Contract, order: Order, orderState: OrderState):
        print(f"openOrder. orderId: {orderId}, contract: {contract}, order: {order}, orderState: {orderState.status}, submitter: {order.submitter}") 

    def orderStatus(self, orderId: TickerId, status: str, filled: Decimal, remaining: Decimal, avgFillPrice: float, permId: TickerId, parentId: TickerId, lastFillPrice: float, clientId: TickerId, whyHeld: str, mktCapPrice: float):
        print(orderId, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice)

    def error(self, reqId: TickerId, errorTime: int, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(f"Error for {reqId}, Time of Error: {errorTime}, Error Code: {errorCode}, Error Message: {errorString}")
        if advancedOrderRejectJson != "":
            print(f"AdvancedOrderRejectJson: {advancedOrderRejectJson}")
            
app = TestApp()
app.connect(host="127.0.0.1", port=7497, clientId=0)
app.run()