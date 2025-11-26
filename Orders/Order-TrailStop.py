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
        
        # Adjusted trail limit
        order = Order()
        order.orderId = orderId
        order.action = "SELL"
        order.orderType = "TRAIL"
        order.tif = "DAY"
        order.totalQuantity = 100
        order.trailStopPrice = 200 
        order.trailingPercent = 5.5

        '''
        You must specify one value: limit price or limit price offset value.
        '''
        order.lmtPrice = 222
        order.lmtPriceOffset = 0.03

        self.placeOrder(order.orderId, mycontract, order)


    def openOrder(self, orderId: OrderId, contract: Contract, order: Order, orderState: OrderState):
        print(f"openOrder. orderId: {orderId}, contract: {contract}, order: {order}") 
        print(f"Maintenance Margin: {orderState.maintMarginAfter}, {orderState.maintMarginBefore}, {orderState.maintMarginChange}")
        print(f"Initial Margin: {orderState.initMarginAfter}, {orderState.initMarginBefore}, {orderState.initMarginChange}")


    def orderStatus(self, orderId: OrderId, status: str, filled: Decimal, remaining: Decimal, avgFillPrice: float, permId: int, parentId: int, lastFillPrice: float, clientId: int, whyHeld: str, mktCapPrice: float):
        print(f"orderId: {orderId}, status: {status}, filled: {filled}, remaining: {remaining}, avgFillPrice: {avgFillPrice}, permId: {permId}, parentId: {parentId}, lastFillPrice: {lastFillPrice}, clientId: {clientId}, whyHeld: {whyHeld}, mktCapPrice: {mktCapPrice}")

    def error(self, reqId: TickerId, errorTime: int, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(f"Error., Time of Error: {errorTime}, Error Code: {errorCode}, Error Message: {errorString}")
        if advancedOrderRejectJson != "":
            print(f"AdvancedOrderRejectJson: {advancedOrderRejectJson}")
        
app = TestApp()
app.connect("127.0.0.1", port, 0)
app.run()