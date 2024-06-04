from decimal import Decimal
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
        mycontract.symbol = "SPX"
        mycontract.secType = "BAG"
        mycontract.currency = "USD"
        mycontract.exchange = "SMART"

        myorder = Order()
        myorder.orderId = orderId
        myorder.action = "BUY"
        myorder.orderType = "LMT"
        myorder.totalQuantity = 1
        myorder.smartComboRoutingParams = []
        myorder.smartComboRoutingParams.append(TagValue("NonGuaranteed", "1"))

        leg1 = ComboLeg()
        leg1.conId = 689492355 # SPX JUN 20 5285 P
        leg1.ratio = 1
        leg1.action = "BUY"
        leg1.exchange = "SMART"

        orderLeg1 = OrderComboLeg()
        orderLeg1.price = 62.80

        leg2 = ComboLeg()
        leg2.conId = 689492203 # SPX JUN 20 5285 C
        leg2.ratio = 1
        leg2.action = "BUY"
        leg2.exchange = "SMART"

        orderLeg2 = OrderComboLeg()
        orderLeg2.price = 63.90
        
        mycontract.comboLegs = [leg1, leg2]
        # myorder.orderComboLegs = [orderLeg1, orderLeg2]
        myorder.orderComboLegs = [orderLeg2, orderLeg1]


        self.placeOrder(myorder.orderId, mycontract, myorder)

    def openOrder(
        self,
        orderId: OrderId,
        contract: Contract,
        order: Order,
        orderState: OrderState,
    ):
        print(
            "openOrder.",
            f"orderId:{orderId}",
            f"contract:{contract}",
            f"order:{order}",
            # f"orderState:{orderState}",
        )

    def orderStatus(
        self,
        orderId: OrderId,
        status: str,
        filled: Decimal,
        remaining: Decimal,
        avgFillPrice: float,
        permId: int,
        parentId: int,
        lastFillPrice: float,
        clientId: int,
        whyHeld: str,
        mktCapPrice: float,
    ):
        print(
            "orderStatus.",
            f"orderId:{orderId}",
            f"status:{status}",
            f"filled:{filled}",
            f"remaining:{remaining}",
            f"avgFillPrice:{avgFillPrice}",
            # f"permId:{permId}",
            f"parentId:{parentId}",
            f"lastFillPrice:{lastFillPrice}",
            # f"clientId:{clientId}",
            # f"whyHeld:{whyHeld}",
            # f"mktCapPrice:{mktCapPrice}",
        )


app = TestApp()
app.connect("127.0.0.1", port, 1001)
app.run()
