from decimal import Decimal
from ibapi.client import *
from ibapi.wrapper import *
from ibapi.contract import *
import time
port = 7496


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):

        # Stock Hedge
        parent = Contract()
        parent.conId = 265598 # AAPL STK
        parent.exchange = "SMART"
        parent.currency = "USD"

        # FX Pair
        hedgeChild = Contract()
        hedgeChild.conId = 14433401 # AUD.USD fx pair
        hedgeChild.exchange = "IDEALPRO"
        hedgeChild.currency = "USD"

        ###################################### Parent Order ###################################################
        parentOrder = Order()
        parentOrder.orderId = orderId
        parentOrder.action = "BUY"
        parentOrder.orderType = "LMT"
        parentOrder.lmtPrice = 145
        parentOrder.totalQuantity = 4
        parentOrder.transmit = False

        
        ###################################### Hedged Child Order ###################################################
        hedgeChildOrder = Order()
        hedgeChildOrder.parentId = parentOrder.orderId
        hedgeChildOrder.orderId = parentOrder.orderId + 1
        hedgeChildOrder.action = "SELL"
        hedgeChildOrder.orderType = "REL"
        hedgeChildOrder.hedgeType = "F"
        hedgeChildOrder.totalQuantity = 0
        hedgeChildOrder.dontUseAutoPriceForHedge = False
        hedgeChildOrder.transmit = True

        ###################################### Executions ###################################################
        self.placeOrder(parentOrder.orderId, parent, parentOrder)
        time.sleep(1)
        self.placeOrder(hedgeChildOrder.orderId, hedgeChild, hedgeChildOrder)


    def openOrder(self, orderId: OrderId, contract: Contract, order: Order, orderState: OrderState):
        print("OpenOrder.",orderId, contract, order, orderState)
    
    def orderStatus(self, orderId: OrderId, status: str, filled: Decimal, remaining: Decimal, avgFillPrice: float, permId: int, parentId: int, lastFillPrice: float, clientId: int, whyHeld: str, mktCapPrice: float):
        print("OrderStatus.",orderId, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice)
    
    def error(self, reqId: TickerId, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print("Error.",reqId, errorCode, errorString, advancedOrderRejectJson)



app = TestApp()
app.connect("127.0.0.1", port, 1001)
app.run()
