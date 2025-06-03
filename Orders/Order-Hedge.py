from ibapi.client import *
from ibapi.wrapper import *
from datetime import datetime
import time
port = 7496


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        print(f"nextValidId. orderId={orderId}")

        # Stock Hedge
        parent = Contract()
        parent.conId = 374570709 # CGP - PARENT
        parent.exchange = "SMART"
        parent.currency = "CAD"

        hedgeChild = Contract()
        hedgeChild.conId = 282158487 # SOLG - To be hedged - CHILD
        hedgeChild.exchange = "SMART"
        hedgeChild.currency = "CAD"

        ###################################### Parent Order ###################################################
        parentOrder = Order()
        parentOrder.orderId = orderId
        parentOrder.action = "BUY"
        parentOrder.orderType = "LMT"
        parentOrder.lmtPrice = 3.37
        parentOrder.totalQuantity = 4
        parentOrder.transmit = False

        
        ###################################### Hedged Child Order ###################################################

        hedgeChildOrder = Order()
        hedgeChildOrder.orderId = parentOrder.orderId + 1
        hedgeChildOrder.action = "SELL"
        hedgeChildOrder.orderType = "LMT"
        hedgeChildOrder.lmtPrice = 0.50
        hedgeChildOrder.hedgeType = "P"
        hedgeChildOrder.dontUseAutoPriceForHedge = True
        hedgeChildOrder.hedgeParam = 1
        hedgeChildOrder.parentId = parentOrder.orderId
        hedgeChildOrder.transmit = True
        ###################################### Executions ###################################################
        
        self.placeOrder(parentOrder.orderId, parent, parentOrder)
        time.sleep(1)
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
