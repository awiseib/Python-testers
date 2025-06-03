from ibapi.client import *
from ibapi.wrapper import *
from ibapi.contract import *
import time

port = 7496

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        ###################################### Contracts ###################################################
        parent = Contract()
        parent.conId = 29831612      #DPZ (Domino's Pizza)
        parent.exchange = "SMART"

        hedgeChild = Contract()
        hedgeChild.conId = 273538    #PZZA (Papa John's)
        hedgeChild.exchange = "SMART"
        
        ###################################### Parent Order ###################################################
        parentOrder = Order()
        parentOrder.orderId = orderId
        parentOrder.action = "BUY"
        parentOrder.orderType = "MKT"
        #parentOrder.orderType = "LMT"
        #parentOrder.lmtPrice = 515
        
        parentOrder.totalQuantity = 1
        parentOrder.transmit = False
        #parentOrder.account = ""
        ###################################### Hedged Child Order ###################################################
        hedgeChildOrder = Order()
        hedgeChildOrder.orderId = orderId + 1
        hedgeChildOrder.parentId = orderId
        hedgeChildOrder.action = "SELL"
        hedgeChildOrder.orderType = "MKT"
        hedgeChildOrder.totalQuantity = 0
        hedgeChildOrder.hedgeType = "P"        #P for Pair Trade
        hedgeChildOrder.hedgeParam = 5         #Hedge Ratio
        hedgeChildOrder.transmit = True
        #hedgeChildOrder.account = ""
        ###################################### Executions ###################################################
        
        self.placeOrder(parentOrder.orderId, parent, parentOrder)
        time.sleep(.2)
        self.placeOrder(hedgeChildOrder.orderId, hedgeChild, hedgeChildOrder)


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