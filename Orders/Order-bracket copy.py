from decimal import Decimal
from ibapi.client import *
from ibapi.wrapper import *
from ibapi.tag_value import TagValue
from ibapi.contract import ComboLeg

port = 7496


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        print(f"nextValidId. orderId={orderId}")

        stockCon = Contract()
        stockCon.symbol = "AAPL"
        stockCon.secType = "BAG"
        stockCon.exchange = "SMART"
        stockCon.currency = "USD"

        leg1 = ComboLeg()
        leg1.conId = 605970527 # call
        leg1.ratio = 1
        leg1.action = "SELL"
        leg1.exchange = "SMART"

        leg2 = ComboLeg()
        leg2.conId = 605970607 # put
        leg2.ratio = 1
        leg2.action = "BUY"
        leg2.exchange = "SMART"

        leg3 = ComboLeg()
        leg3.conId = 265598 # put
        leg3.ratio = 100
        leg3.action = "BUY"
        leg3.exchange = "SMART"

        stockCon.comboLegs = []
        stockCon.comboLegs.append(leg1)
        stockCon.comboLegs.append(leg2)
        stockCon.comboLegs.append(leg3)

        stkOrder = Order()
        stkOrder.orderId = orderId
        stkOrder.action = "BUY"
        stkOrder.orderType = "LMT"
        stkOrder.totalQuantity = 1
        stkOrder.lmtPrice = 152.25

        self.placeOrder(orderId, stockCon, stkOrder)

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
        stkOrderId: int,
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
            f"stkOrderId:{stkOrderId}",
            f"lastFillPrice:{lastFillPrice}",
            # f"clientId:{clientId}",
            # f"whyHeld:{whyHeld}",
            # f"mktCapPrice:{mktCapPrice}",
        )

    def error(self, reqId: TickerId, errorCode: int, errorString: str, tickAttrib):
        print(f"error. reqId:{reqId} code:{errorCode} string:{errorString}")


app = TestApp()
app.connect("127.0.0.1", 7496, 1001)
app.run()
