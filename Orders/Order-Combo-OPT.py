from ibapi.client import *
from ibapi.wrapper import *
from ibapi.contract import ComboLeg
from ibapi.order import *

port = 7496


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        mycontract = Contract()
        mycontract.symbol = "SPX" # Designate the symbols of both contracts in the combo.
        mycontract.secType = "BAG" # BAG must always be used to designate a combo order.
        mycontract.currency = "USD"
        mycontract.exchange = "SMART"

        leg1 = ComboLeg()
        leg1.conId = 681176151 # SPX FEB 5850 C
        leg1.ratio = 1 # The leg's ration will be 1. This means leg1 will purchase (totalQuantiy * 1) shares.
        leg1.action = "BUY"
        leg1.exchange = "SMART"

        leg2 = ComboLeg()
        leg2.conId = 724011409 # SPX FEB 5875 C
        leg2.ratio = 1 # The leg's ratio will be 10. This means leg2 will purchase (totalQuantity * 10) shares
        leg2.action = "Sell"
        leg2.exchange = "SMART"

        leg3 = ComboLeg()
        leg3.conId = 736845869 # SPX FEB 5875 C
        leg3.ratio = 1 # The leg's ratio will be 10. This means leg2 will purchase (totalQuantity * 10) shares
        leg3.action = "BUY"
        leg3.exchange = "SMART"

        leg4 = ComboLeg()
        leg4.conId = 724012971 # SPX FEB 5875 C
        leg4.ratio = 1 # The leg's ratio will be 10. This means leg2 will purchase (totalQuantity * 10) shares
        leg4.action = "Sell"
        leg4.exchange = "SMART"

        mycontract.comboLegs = []
        mycontract.comboLegs.append(leg1)
        mycontract.comboLegs.append(leg2)
        mycontract.comboLegs.append(leg3)
        mycontract.comboLegs.append(leg4)
        

        myorder = Order()
        myorder.orderId = orderId
        myorder.action = "BUY"
        myorder.tif = "DAY"
        # myorder.goodTillDate = "20241206-16:50:00"
        # myorder.outsideRth = True
        myorder.totalQuantity = 1 # This is the total number of combinations to buy. This example will result with me owning 1 SPX option and 10 SPY options.

        myorder.orderType = "LMT" # Combos support a variety of order types, including LMT, MKT, and STP.
        # myorder.smartComboRoutingParams = [TagValue("NonGuaranteed", "0")]
        '''
        The pricing structure for combo orders is based on the total value of all legs.
        In this case:
            We are buying 1 SPX option, currently trading at about $180.
            We are buying 10 SPY options, currently trading at about $14.
            ($180 * 1)  +   ($14 * 10)  =   320
            180         +   140         =   320
        '''
        myorder.lmtPrice = -0.45

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
