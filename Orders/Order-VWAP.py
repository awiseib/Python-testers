from decimal import Decimal
from ibapi.tag_value import TagValue
from ibapi.client import *
from ibapi.wrapper import *
from datetime import datetime
from ibapi.contract import *
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
        order.totalQuantity = 1
        order.orderType = "IBALGO"
        # order.lmtPrice = 100
        order.algoStrategy = "Vwap"

        order.algoParams = []
        order.algoParams.append(TagValue("maxPctVol", .3))
        order.algoParams.append(TagValue("startTime", "13:15:00 US/Eastern"))
        order.algoParams.append(TagValue("endTime", "20230415 15:30:00 US/Eastern"))
        order.algoParams.append(TagValue("allowPastEndTime",int(0)))
        order.algoParams.append(TagValue("noTakeLiq", int(0)))

        #order.algoParams.append(TagValue("monetaryValue", monetaryValue))

        self.placeOrder(orderId, contract, order)

    # def marketRule(self, marketRuleId: int, priceIncrements: ListOfPriceIncrements):
    #     print("Market Rule details: ", marketRuleId, priceIncrements)

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
            # "\n",
            # f"Margin Values: \n",
            # f"initMarginBefore: {orderState.initMarginBefore}; initMarginAfter: {orderState.initMarginAfter};initMarginChange: {orderState.initMarginChange}; \n",
            # f"maintMarginBefore: {orderState.maintMarginBefore }; maintMarginAfter: {orderState.maintMarginAfter};maintMarginChange: {orderState.maintMarginChange}; \n",
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

