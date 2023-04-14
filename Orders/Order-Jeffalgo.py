from ibapi.client import *
from ibapi.wrapper import *
from ibapi.tag_value import TagValue
from datetime import datetime
import time

port = 7496

# ! [jefferies_vwap_params]
def FillJefferiesVWAPParams(baseOrder: Order, startTime: str,
                            endTime: str, relativeLimit: float,
                            maxVolumeRate: float, excludeAuctions: str,
                            triggerPrice: float, wowPrice: float,
                            minFillSize: int, wowOrderPct: float,
                            wowMode: str, isBuyBack: bool, wowReference: str):
    # must be direct-routed to "JEFFALGO"
    baseOrder.algoStrategy = "VWAP"
    baseOrder.algoParams = []
    baseOrder.algoParams.append(TagValue("StartTime", startTime))
    baseOrder.algoParams.append(TagValue("EndTime", endTime))
    baseOrder.algoParams.append(TagValue("RelativeLimit", relativeLimit))
    baseOrder.algoParams.append(TagValue("MaxVolumeRate", maxVolumeRate))
    baseOrder.algoParams.append(TagValue("ExcludeAuctions", excludeAuctions))
    baseOrder.algoParams.append(TagValue("TriggerPrice", triggerPrice))
    baseOrder.algoParams.append(TagValue("WowPrice", wowPrice))
    baseOrder.algoParams.append(TagValue("MinFillSize", minFillSize))
    baseOrder.algoParams.append(TagValue("WowOrderPct", wowOrderPct))
    baseOrder.algoParams.append(TagValue("WowMode", wowMode))
    baseOrder.algoParams.append(TagValue("IsBuyBack", int(isBuyBack)))
    baseOrder.algoParams.append(TagValue("WowReference", wowReference))
    return baseOrder
# ! [jefferies_vwap_params]

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):

        mycontract = Contract()
        mycontract.symbol = "AAPL"
        mycontract.secType = "STK"
        mycontract.currency = "USD"
        mycontract.exchange = "JEFFALGO" # Jefferies algo orders must be direct-routed to JEFFALGO

        baseOrder = Order()
        baseOrder.action = "BUY"
        baseOrder.totalQuantity = 10
        baseOrder.orderType = "LMT"
        baseOrder.lmtPrice = 145

        # ! [jeff_vwap_algo]
        baseOrder = FillJefferiesVWAPParams(baseOrder, "10:00:00 US/Eastern", "16:00:00 US/Eastern", 10, 10, "Exclude_Both", 130, 135, 1, 10, "Patience", False, "Midpoint")
        self.placeOrder(orderId, mycontract, baseOrder)
        # ! [jeff_vwap_algo]


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

    def error(
        self,
        reqId: TickerId,
        errorCode: int,
        errorString: str,
        advancedOrderRejectJson="",
    ):
        print(
            datetime.now().strftime("%H:%M:%S.%f")[:-3],
            "error.",
            f"reqId:{reqId}",
            f"errorCode:{errorCode}",
            f"errorString:{errorString}",
            f"advancedOrderRejectJson:{advancedOrderRejectJson}",
        )


app = TestApp()
app.connect("127.0.0.1", port, 1001)
app.run()
