from decimal import Decimal
from ibapi.client import *
from ibapi.wrapper import *
from datetime import datetime
from ibapi.contract import *
from ibapi.order_state import *

port = 7496


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        print(f"nextValidId. orderId={orderId}")

        parentContract = Contract() 
        parentContract.conId = 265598 # AAPL Options
        parentContract.exchange = "SMART"
        parentContract.currency = "USD"

        child1 = Contract() 
        child1.conId = 265598 # AAPL Options
        child1.exchange = "SMART"
        child1.currency = "USD"

        child2 = Contract() 
        child2.conId = 265598 # AAPL Options
        child2.exchange = "SMART"
        child2.currency = "USD"

        parentOrder = Order()
        parentOrder.orderId = orderId
        parentOrder.action = "BUY"
        parentOrder.orderType = "LMT"
        parentOrder.lmtPrice = 154.50
        parentOrder.totalQuantity = 1

        parentOrder.ocaGroup = "TestOCA_", orderId
        parentOrder.ocaType = 1

        parentOrder.faGroup = "equalQty_test"
        parentOrder.faMethod = "Equal"

        chilldO1 = Order()
        chilldO1.orderId = orderId + 1
        chilldO1.action = "BUY"
        chilldO1.orderType = "LMT"
        chilldO1.lmtPrice = 154.80
        chilldO1.totalQuantity = 1

        chilldO1.ocaGroup = "TestOCA_", orderId
        chilldO1.ocaType = 1

        chilldO1.faGroup = "equalQty_test"
        chilldO1.faMethod = "Equal"


        chilldO2 = Order()
        chilldO2.orderId = orderId + 2
        chilldO2.action = "BUY"
        chilldO2.orderType = "LMT"
        chilldO2.lmtPrice = 155.00
        chilldO2.totalQuantity = 1

        chilldO2.ocaGroup = "TestOCA_", orderId
        chilldO2.ocaType = 1

        chilldO2.faGroup = "equalQty_test"
        chilldO2.faMethod = "Equal"

        self.placeOrder(orderId, parentContract, parentOrder)
        self.placeOrder(chilldO1.orderId, child1, chilldO1)
        self.placeOrder(chilldO2.orderId, child2, chilldO2)


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
