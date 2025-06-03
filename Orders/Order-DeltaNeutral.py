from ibapi.client import *
from ibapi.wrapper import *
from ibapi.contract import ComboLeg, DeltaNeutralContract

port = 7496


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        print(f"nextValidId. orderId={orderId}")

        # Create a BAG contract with underlying symbol
        mycontract = Contract()
        mycontract.symbol = "AAPL"
        mycontract.secType = "BAG"
        mycontract.exchange = "SMART"
        mycontract.currency = "USD"

        # Create 1 or more legs of this BAG/combo instrument.
        # This is a random AAPL call. You can create an option spread
        # here as normal, and this method of delta hedging still applies.
        leg1 = ComboLeg()
        leg1.conId = 502056585
        leg1.ratio = 1
        leg1.action = "BUY"
        leg1.exchange = "SMART"

        # leg2 = ComboLeg()
        # leg2.conId = 531781574
        # leg2.ratio = 1
        # leg2.action = "SELL"
        # leg2.exchange = "SMART"

        mycontract.comboLegs = []
        mycontract.comboLegs.append(leg1)
        # mycontract.comboLegs.append(leg2)

        # Now we create a special kind of delta hedge contract, which
        # will be attached to the above combo.
        # This object can take three parameters, only one of which is
        # required: the conId of the underlying with which to hedge. 
        dn = DeltaNeutralContract()
        dn.conId = 265598 # AAPL stock conId, required attribute

        # You may specify a particular delta here.
        # If no delta is specified, this will default to a delta of 1.0,
        # so the 
        dn.delta = 35
        # dn.price = 160.03 # you can specify a particular underlying price

        mycontract.deltaNeutralContract = dn

        myorder = Order()
        myorder.orderId = orderId
        myorder.action = "BUY"
        myorder.orderType = "LMT"
        myorder.totalQuantity = 1.0
        myorder.lmtPrice = 158.20
        myorder.tif = "GTC"
        myorder.outsideRth = True
        myorder.orderRef = "delta_neutral"

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
