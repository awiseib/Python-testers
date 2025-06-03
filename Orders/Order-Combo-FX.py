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
        mycontract.symbol = "EUR,GBP,USD"
        mycontract.secType = "BAG"
        mycontract.currency = "USD"
        mycontract.exchange = "SMART"

        leg1 = ComboLeg()
        leg1.conId = 12087792 
        leg1.ratio = 1
        leg1.action = "BUY"
        leg1.exchange = "IDEALPRO"

        leg2 = ComboLeg()
        leg2.conId = 12087797 
        leg2.ratio = 1
        leg2.action = "BUY"
        leg2.exchange = "IDEALPRO"

        leg2 = ComboLeg()
        leg2.conId = 12087807 
        leg2.ratio = 1
        leg2.action = "BUY"
        leg2.exchange = "IDEALPRO"

        mycontract.comboLegs = []
        mycontract.comboLegs.append(leg1)
        mycontract.comboLegs.append(leg2)
        

        myorder = Order()
        myorder.orderId = orderId
        myorder.action = "BUY"
        myorder.orderType = "LMT"
        myorder.totalQuantity = 1000

        myorder.lmtPrice = -80

        myorder.smartComboRoutingParams = []
        myorder.smartComboRoutingParams.append(TagValue("NonGuaranteed", "0"))


        self.placeOrder(myorder.orderId, mycontract, myorder)

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
