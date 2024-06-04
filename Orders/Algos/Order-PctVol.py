from ibapi.client import *
from ibapi.wrapper import *
from ibapi.tag_value import TagValue
from datetime import datetime

port = 7496


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):

        mycontract = Contract()
        mycontract.conId = 265598
        mycontract.exchange = "SMART"
        
        myorder = Order()
        myorder.action = "BUY"
        myorder.orderType = "LMT"
        myorder.lmtPrice = 187
        myorder.totalQuantity = 50
        
        myorder.algoStrategy = "PctVol"
        myorder.algoParams = []
        myorder.algoParams.append(TagValue("pctVol", "0.5"))
        myorder.algoParams.append(TagValue("startTime", "09:00:00 US/Eastern"))
        myorder.algoParams.append(TagValue("endTime", "14:00:00 US/Eastern"))
        myorder.algoParams.append(TagValue("noTakeLiq", "1"))

        self.placeOrder(orderId, mycontract, myorder)

    def openOrder(
        self,
        orderId: OrderId,
        contract: Contract,
        order: Order,
        orderState: OrderState,
    ):
        print(
            datetime.now().strftime("%H:%M:%S.%f")[:-3],
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
            datetime.now().strftime("%H:%M:%S.%f")[:-3],
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

    def error(self, reqId: TickerId, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print("ERROR: ",errorCode, errorString)


app = TestApp()
app.connect("127.0.0.1", port, 1001)
app.run()
