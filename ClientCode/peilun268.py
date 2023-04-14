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
        mycontract.symbol = "AMD"
        mycontract.secType = "BAG"
        mycontract.currency = "USD"
        mycontract.exchange = "SMART"

        leg1 = ComboLeg()
        leg1.conId = 606842224 # 85 C
        leg1.ratio = 1
        leg1.action = "BUY"
        leg1.exchange = "SMART"

        leg2 = ComboLeg()
        leg2.conId = 606842348 # 85 P
        leg2.ratio = 1
        leg2.action = "SELL"
        leg2.exchange = "SMART"

        leg3 = ComboLeg()
        leg3.conId = 606516019 # 65 C
        leg3.ratio = 1
        leg3.action = "SELL"
        leg3.exchange = "SMART"

        leg4 = ComboLeg()
        leg4.conId = 606517203 # 65 P
        leg4.ratio = 1
        leg4.action = "BUY"
        leg4.exchange = "SMART"

        mycontract.comboLegs = []
        mycontract.comboLegs.append(leg1)
        mycontract.comboLegs.append(leg2)
        mycontract.comboLegs.append(leg3)
        mycontract.comboLegs.append(leg4)
        

        myorder = Order()
        myorder.orderId = orderId
        myorder.orderType = "LMT"
        myorder.action = "BUY"
        # myorder.lmtPrice = -19.83
        # myorder.action = "SELL"
        myorder.lmtPrice = 19.83
        myorder.totalQuantity = 5

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
