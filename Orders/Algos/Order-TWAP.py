from decimal import Decimal
from ibapi.tag_value import TagValue
from ibapi.client import *
from ibapi.wrapper import *
from datetime import datetime

port = 7496


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        contract = Contract()
        contract.symbol = "AAPL"
        contract.secType = "STK"
        contract.exchange = "SMART"
        contract.currency = "USD"
        
        order = Order()
        order.action = "BUY"
        order.totalQuantity = 10
        order.orderType = "LMT" # 
        order.lmtPrice = 220
        order.tif = "DAY"
        order.algoStrategy = "Twap"

        order.algoParams = []
        order.algoParams.append(TagValue("startTime", "20240813-17:00:00"))
        order.algoParams.append(TagValue("endTime", "20240813-18:00:00"))
        order.algoParams.append(TagValue("allowPastEndTime", 0))
        order.algoParams.append(TagValue("catchUp", 0))
        
        self.placeOrder(orderId, contract, order)


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
            f"parentId:{parentId}",
            f"lastFillPrice:{lastFillPrice}",
        )
    
    def openOrderEnd(self):
        pass

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
app.connect("127.0.0.1", port, 1006)
app.run()

