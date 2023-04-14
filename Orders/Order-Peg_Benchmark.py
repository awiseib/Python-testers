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
        print(f"nextValidId. orderId={orderId}")

        mycontract = Contract()
        mycontract.conId = 422302967 # TMBR STK
        mycontract.exchange = "SMART"
        mycontract.currency = "USD"

        myorder = Order()
        myorder.orderId = orderId
        myorder.orderType = "PEG BENCH"
        # BUY or SELL
        myorder.action = "BUY"
        myorder.totalQuantity = 10000
        #Beginning with price...
        # myorder.startingPrice = 12.60
        #increase/decrease price..
        myorder.isPeggedChangeAmountDecrease = True
        #by... (and likewise for price moving in opposite direction)
        myorder.peggedChangeAmount = 0.001
        #whenever there is a price change of...
        myorder.referenceChangeAmount = 0.001
        #in the reference contract...
        myorder.referenceContractId = 47605491 # IGF STK
        #being traded at...
        myorder.referenceExchangeId = "SMART"
        #starting reference price is...
        myorder.stockRefPrice = 46.74
        #Keep myorder active as long as reference contract trades between...
        myorder.stockRangeLower = 43.00
        #and...
        myorder.stockRangeUpper = 49.00

        self.placeOrder(myorder.orderId, mycontract, myorder)

    def marketRule(self, marketRuleId: int, priceIncrements: ListOfPriceIncrements):
        print("Market Rule details: ", marketRuleId, priceIncrements)

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
            f"orderState:{orderState}",
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
        self.disconnect()

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

