from decimal import Decimal
from ibapi.client import *
from ibapi.wrapper import *
from ibapi.tag_value import TagValue
from ibapi.contract import ComboLeg
from ibapi.order import *

port = 7496


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        mycontract = Contract()
        mycontract.symbol = "AAPL,TSLA"
        mycontract.secType = "BAG"
        mycontract.currency = "USD"
        mycontract.exchange = "SMART"
        leg1 = ComboLeg()
        leg1.conId = 265598 
        leg1.ratio = 1
        leg1.action = "BUY"
        leg1.exchange = "SMART"
        leg2 = ComboLeg()
        leg2.conId = 76792991 
        leg2.ratio = 1
        leg2.action = "SELL"
        leg2.exchange = "SMART"
        mycontract.comboLegs = []
        mycontract.comboLegs.append(leg1)
        mycontract.comboLegs.append(leg2)

        parent = Order()
        parent.orderId = orderId
        parent.action = "BUY"
        parent.orderType = "MKT"
        parent.totalQuantity = 10
        #parent.lmtPrice = parent_price
        parent.transmit = False
        parent.smartComboRoutingParams = [TagValue("NonGuaranteed", "1")]


        profit_taker = Order()
        profit_taker.orderId = parent.orderId + 1
        profit_taker.parentId = parent.orderId
        profit_taker.action = "SELL" if parent.action == "BUY" else "BUY"
        profit_taker.orderType = "LMT"
        profit_taker.totalQuantity = 10
        #profit_taker.lmtPrice = parent_price + 1.0
        profit_taker.lmtPrice = -80
        profit_taker.transmit = False
        profit_taker.smartComboRoutingParams = [TagValue("NonGuaranteed", "1")]

        stop_loss = Order()
        stop_loss.orderId = parent.orderId + 2
        stop_loss.parentId = parent.orderId
        stop_loss.action = "SELL" if parent.action == "BUY" else "BUY"
        stop_loss.orderType = "STP"
        stop_loss.totalQuantity = 10
        #stop_loss.auxPrice = parent_price - 1.0
        stop_loss.auxPrice = -50
        stop_loss.transmit = True
        stop_loss.smartComboRoutingParams = [TagValue("NonGuaranteed", "1")]

        self.placeOrder(parent.orderId, mycontract, parent)
        self.placeOrder(profit_taker.orderId, mycontract, profit_taker)
        self.placeOrder(stop_loss.orderId, mycontract, stop_loss)

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
