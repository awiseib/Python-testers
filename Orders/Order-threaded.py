from ibapi.client import *
from ibapi.wrapper import *
import threading
import time

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)
        # self.nextOrderId = 0

    def nextValidId(self, orderId: OrderId):
        super().nextValidId(orderId)
        self.nextOrderId = orderId
        


    def openOrder(self, orderId: OrderId, contract: Contract, order: Order, orderState: OrderState):
        print(f"openOrder. orderId: {orderId}, contract: {contract}, order: {order}") 
        print(f"Maintenance Margin: {orderState.maintMarginAfter}, {orderState.maintMarginBefore}, {orderState.maintMarginChange}")
        print(f"Initial Margin: {orderState.initMarginAfter}, {orderState.initMarginBefore}, {orderState.initMarginChange}")


    def orderStatus(self, orderId: OrderId, status: str, filled: Decimal, remaining: Decimal, avgFillPrice: float, permId: int, parentId: int, lastFillPrice: float, clientId: int, whyHeld: str, mktCapPrice: float):
        print(f"orderId: {orderId}, status: {status}, filled: {filled}, remaining: {remaining}, avgFillPrice: {avgFillPrice}, permId: {permId}, parentId: {parentId}, lastFillPrice: {lastFillPrice}, clientId: {clientId}, whyHeld: {whyHeld}, mktCapPrice: {mktCapPrice}")


    def execDetails(self, reqId: int, contract: Contract, execution: Execution):
        print(f"reqId: {reqId}, contract: {contract}, execution: {execution}")

app = TestApp()
app.connect("127.0.0.1", 7496, 100)
threading.Thread(target=app.run).start()

app.reqCurrentTime()
# time.sleep(3)
mycontract = Contract()
mycontract.symbol = "AAPL"
mycontract.secType = "STK"    
mycontract.exchange = "SMART"
mycontract.currency = "USD"
time.sleep(1)
print(app.nextOrderId)

myorder = Order()
myorder.orderId = app.nextOrderId
myorder.action = "BUY"
myorder.orderType = "MKT"
myorder.totalQuantity = 10

app.placeOrder(myorder.orderId, mycontract, myorder)