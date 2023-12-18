from ibapi.client import *
from ibapi.wrapper import *
import time
port=7496

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):

        mycontract = Contract()
        mycontract.conId = 265598 # AAPL Conid
        mycontract.exchange = "SMART"

        myorder = Order()
        myorder.action = "BUY"
        myorder.tif = "GTC"
        myorder.orderType = "LMT"
        myorder.lmtPrice = 180
        myorder.outsideRth = True
        myorder.totalQuantity = 5

        self.placeOrder(orderId, mycontract, myorder)

    def openOrder(self, orderId: OrderId, contract: Contract, order: Order, orderState: OrderState):
        print(f"openOrder. orderId: {orderId}, contract: {contract}, order: {order}") 
        print(f"Maintenance Margin: {orderState.maintMarginAfter}, {orderState.maintMarginBefore}, {orderState.maintMarginChange}")
        print(f"Initial Margin: {orderState.initMarginAfter}, {orderState.initMarginBefore}, {orderState.initMarginChange}")


    def orderStatus(self, orderId: OrderId, status: str, filled: Decimal, remaining: Decimal, avgFillPrice: float, permId: int, parentId: int, lastFillPrice: float, clientId: int, whyHeld: str, mktCapPrice: float):
        print(f"orderId: {orderId}, status: {status}, filled: {filled}, remaining: {remaining}, avgFillPrice: {avgFillPrice}, permId: {permId}, parentId: {parentId}, lastFillPrice: {lastFillPrice}, clientId: {clientId}, whyHeld: {whyHeld}, mktCapPrice: {mktCapPrice}")


    def execDetails(self, reqId: int, contract: Contract, execution: Execution):
        print(f"reqId: {reqId}, contract: {contract}, execution: {execution}")

    def error(self, reqId: TickerId, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print("Error", reqId, errorCode, errorString, advancedOrderRejectJson)

app = TestApp()
app.connect("127.0.0.1", port, 0)
app.run()