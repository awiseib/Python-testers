from ibapi.client import *
from ibapi.wrapper import *
from ibapi.tag_value import TagValue
from datetime import datetime
import time

port = 7496


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        print(f"nextValidId. orderId={orderId}")
        order_id = orderId

        mycontract = Contract()
        mycontract.symbol = "BMW"
        mycontract.secType = "STK"
        mycontract.exchange = "SMART"
        mycontract.primaryExchange = "IBIS"
        mycontract.currency = "EUR"
        
        myorder = Order()
        myorder.action = "BUY"
        myorder.orderType = "LMT"
        myorder.lmtPrice = 95
        myorder.totalQuantity = 50
        myorder.tif = "DAY"
        myorder.algoStrategy = "ArrivalPx"
        myorder.algoParams = []
        myorder.algoParams.append(TagValue("maxPctVol", 0.1))
        myorder.algoParams.append(TagValue("riskAversion", "Aggressive"))
        myorder.algoParams.append(TagValue("startTime", "12:00:00 UTC"))
        myorder.algoParams.append(TagValue("endTime", "13:00:00 UTC"))
        myorder.algoParams.append(TagValue("allowPastEndTime",1))
        myorder.algoParams.append(TagValue("forceCompletion",0))

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
        print("ERROR: ", errorString)


app = TestApp()
app.connect("127.0.0.1", port, 1001)
app.run()
