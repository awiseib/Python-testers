from ibapi.client import *
from ibapi.common import Decimal, OrderId, TickerId
from ibapi.contract import Contract
from ibapi.order import Order
from ibapi.order_state import OrderState
from ibapi.utils import Decimal
from ibapi.wrapper import *
from ibapi.contract import *
from ibapi.tag_value import TagValue

port = 7496

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):

        mycontract = Contract()
        mycontract.symbol = "TSLA"
        mycontract.secType = "STK"
        mycontract.currency = "USD"
        mycontract.exchange = "SMART" 
        
        baseOrder = Order()
        baseOrder.action = "BUY"
        baseOrder.totalQuantity = 1000
        baseOrder.orderType = "LMT"
        baseOrder.lmtPrice = 230
        baseOrder.tif = "GTC"
        baseOrder.outsideRth = True

        baseOrder.algoStrategy = "AD"
        baseOrder.algoParams = []
        baseOrder.algoParams.append(TagValue("componentSize", 10))
        baseOrder.algoParams.append(TagValue("timeBetweenOrders", 15))
        baseOrder.algoParams.append(TagValue("randomizeTime20", int(1)))
        baseOrder.algoParams.append(TagValue("randomizeSize55", int(1)))
        baseOrder.algoParams.append(TagValue("giveUp", 0))
        baseOrder.algoParams.append(TagValue("catchUp", int(1)))
        baseOrder.algoParams.append(TagValue("waitForFill", int(0)))
        baseOrder.algoParams.append(TagValue("activeTimeStart", "17:54:00"))
        baseOrder.algoParams.append(TagValue("activeTimeEnd", "02:51:00"))

        self.placeOrder(orderId, mycontract, baseOrder)
        # ! [jeff_vwap_algo]


    def openOrder(self, orderId: OrderId, contract: Contract, order: Order, orderState: OrderState):
        print(orderId, contract, order, orderState)
    
    def orderStatus(self, orderId: OrderId, status: str, filled: Decimal, remaining: Decimal, avgFillPrice: float, permId: int, parentId: int, lastFillPrice: float, clientId: int, whyHeld: str, mktCapPrice: float):
        print(orderId, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice)
    
    def error(self, reqId: TickerId, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(reqId, errorCode, errorString, advancedOrderRejectJson)


app = TestApp()
app.connect("127.0.0.1", port, 1001)
app.run()
