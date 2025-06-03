from ibapi.client import *
from ibapi.wrapper import *
from ibapi.tag_value import TagValue
from ibapi.contract import ComboLeg
from ibapi.order import *

'''
NOTE: Combo per-leg prices are only supported for non-guaranteed smart combos with two legs.
    Combos with more than two legs or are guaranteed will not be supported.
'''


port = 7496

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        mycontract = Contract()
        mycontract.symbol = "AAPL,IBM"
        mycontract.secType = "BAG"
        mycontract.currency = "USD"
        mycontract.exchange = "SMART"

        myorder = Order()
        myorder.orderId = orderId
        myorder.action = "BUY"
        myorder.orderType = "LMT"
        myorder.lmtPrice = 111
        myorder.totalQuantity = 1
        myorder.smartComboRoutingParams = []
        myorder.smartComboRoutingParams.append(TagValue("NonGuaranteed", "1"))

        leg1 = ComboLeg()
        leg1.conId = 265598 # SPX JUN 20 5285 P
        leg1.ratio = 1
        leg1.action = "BUY"
        leg1.exchange = "SMART"

        orderLeg1 = OrderComboLeg()
        orderLeg1.price = 222

        leg2 = ComboLeg()
        leg2.conId = 8314 # SPX JUN 20 5285 C
        leg2.ratio = 1
        leg2.action = "BUY"
        leg2.exchange = "SMART"

        orderLeg2 = OrderComboLeg()
        orderLeg2.price = 333
        
        mycontract.comboLegs = [leg1, leg2]
        myorder.orderComboLegs = [orderLeg2, orderLeg1]


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
