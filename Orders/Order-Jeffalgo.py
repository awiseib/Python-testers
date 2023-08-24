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
        mycontract.symbol = "AAPL"
        mycontract.secType = "STK"
        mycontract.currency = "USD"
        mycontract.exchange = "JEFFALGO" # Jefferies algo orders must be direct-routed to JEFFALGO

        baseOrder = Order()
        baseOrder.action = "BUY"
        baseOrder.totalQuantity = 10
        baseOrder.orderType = "LMT"
        baseOrder.lmtPrice = 180
        baseOrder.transmit = False
        
        baseOrder.algoStrategy = "VWAP"
        baseOrder.algoParams = []
        # baseOrder.algoParams.append(TagValue("StartTime", "11:00:00 US/Eastern"))
        # baseOrder.algoParams.append(TagValue("EndTime", "15:59:59 US/Eastern"))
        baseOrder.algoParams.append(TagValue("RelativeLimit", 1))
        baseOrder.algoParams.append(TagValue("MaxVolumeRate", 5))
        baseOrder.algoParams.append(TagValue("ExcludeAuctions", "Exclude_Both"))
        baseOrder.algoParams.append(TagValue("TriggerPrice", 178))
        baseOrder.algoParams.append(TagValue("WoWPrice", 183))
        baseOrder.algoParams.append(TagValue("MinFillSize", 1))
        baseOrder.algoParams.append(TagValue("WoWOrderPct", 0))
        baseOrder.algoParams.append(TagValue("WoWMode", "VWAP_Day"))
        # baseOrder.algoParams.append(TagValue("IsBuyBack", 1))
        baseOrder.algoParams.append(TagValue("WoWReference", "Midpoint"))

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
