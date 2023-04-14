from asyncio.windows_events import NULL
from decimal import Decimal
from pickle import FALSE, TRUE
from queue import PriorityQueue
from threading import Timer
from ibapi.tag_value import TagValue
from tkinter.tix import Tree
from ibapi.client import *
from ibapi.wrapper import *
from datetime import datetime
from ibapi.contract import *
from ibapi.order_condition import Create, OrderCondition
from ibapi.order_state import *
import time

port = 7496


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        contract = Contract()
        contract.symbol = "F"
        contract.secType = "STK"
        contract.exchange = "SMART"
        contract.currency = "USD"
        
        order = Order()
        order.action = "BUY"
        order.totalQuantity = 150
        order.orderType = "LMT"
        order.lmtPrice = 12
        order.tif = "DAY"
        order.algoStrategy = "Twap"

        order.algoParams = []
        # order.algoParams.append(TagValue("strategyType", "Marketable"))
        order.algoParams.append(TagValue("startTime", "12:00:00 America/Chicago"))
        order.algoParams.append(TagValue("endTime", "20220919 15:30:00 America/Chicago"))
        order.algoParams.append(TagValue("allowPastEndTime", 0))
        # order.algoParams.append(TagValue("cashQty", ))
        
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

