from decimal import Decimal
from ibapi.client import *
from ibapi.common import OrderId
from ibapi.order import Order
from ibapi.order_state import OrderState
from ibapi.wrapper import *
from ibapi.contract import ComboLeg, Contract
from ibapi.order import *

port = 7496


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        mycontract = Contract()
        mycontract.symbol = "SPX,SPY" # Designate the symbols of both contracts in the combo.
        mycontract.secType = "BAG" # BAG must always be used to designate a combo order.
        mycontract.currency = "USD"
        mycontract.exchange = "SMART"

        leg1 = ComboLeg()
        leg1.conId = 654370534 # SPX OCT 18 5350 P
        leg1.ratio = 1 # The leg's ration will be 1. This means leg1 will purchase (totalQuantiy * 1) shares.
        leg1.action = "BUY"
        leg1.exchange = "SMART"

        leg2 = ComboLeg()
        leg2.conId = 700892035 # SPY OCT 18 525 P
        leg2.ratio = 10 # The leg's ratio will be 10. This means leg2 will purchase (totalQuantity * 10) shares
        leg2.action = "BUY"
        leg2.exchange = "SMART"

        mycontract.comboLegs = []
        mycontract.comboLegs.append(leg1)
        mycontract.comboLegs.append(leg2)
        

        myorder = Order()
        myorder.orderId = orderId
        myorder.action = "BUY"
        myorder.totalQuantity = 1 # This is the total number of combinations to buy. This example will result with me owning 1 SPX option and 10 SPY options.

        myorder.orderType = "LMT" # Combos support a variety of order types, including LMT, MKT, and STP.

        '''
        The pricing structure for combo orders is based on the total value of all legs.
        In this case:
            We are buying 1 SPX option, currently trading at about $200.
            We are buying 10 SPY options, currently trading at about $14.
            ($180 * 1)  +   ($14 * 10)  =   320
            180         +   140         =   320
        '''
        myorder.lmtPrice = 320

        self.placeOrder(myorder.orderId, mycontract, myorder)

    def openOrder(self, orderId: int, contract: Contract, order: Order, orderState: OrderState):
        print(f"openOrder. orderId:{orderId} contract:{contract} order:{order} orderState:{orderState}")

    def orderStatus(self, orderId: OrderId, status: str, filled: Decimal, remaining: Decimal, avgFillPrice: float, permId: OrderId, parentId: OrderId, lastFillPrice: float, clientId: OrderId, whyHeld: str, mktCapPrice: float):
        print(f"orderStatus. orderId:{orderId} status:{status} filled:{filled} remaining:{remaining} avgFillPrice:{avgFillPrice} permId:{permId} parentId:{parentId} lastFillPrice:{lastFillPrice} clientId:{clientId} whyHeld:{whyHeld} mktCapPrice:{mktCapPrice}")


app = TestApp()
app.connect("127.0.0.1", port, 1001)
app.run()
