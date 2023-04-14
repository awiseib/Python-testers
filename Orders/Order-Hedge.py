from decimal import Decimal
from ibapi.client import *
from ibapi.wrapper import *
from datetime import datetime
from ibapi.contract import *
from ibapi.order_condition import Create, OrderCondition
import time
port = 7496


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        print(f"nextValidId. orderId={orderId}")

        # Stock Hedge
        parent = Contract()
        parent.conId = 374570709 # CGP - PARENT
        parent.exchange = "SMART"
        parent.currency = "CAD"

        hedgeChild = Contract()
        hedgeChild.conId = 282158487 # SOLG - To be hedged - CHILD
        hedgeChild.exchange = "SMART"
        hedgeChild.currency = "CAD"

        ###################################### Parent Order ###################################################
        parentOrder = Order()
        parentOrder.orderId = orderId
        parentOrder.action = "BUY"
        parentOrder.orderType = "LMT"
        parentOrder.lmtPrice = 3.37
        parentOrder.totalQuantity = 4
        parentOrder.transmit = False

        
        ###################################### Hedged Child Order ###################################################

        hedgeChildOrder = Order()
        hedgeChildOrder.orderId = parentOrder.orderId + 1
        hedgeChildOrder.action = "SELL"
        hedgeChildOrder.orderType = "LMT"
        hedgeChildOrder.lmtPrice = 0.50
        hedgeChildOrder.hedgeType = "P"
        hedgeChildOrder.dontUseAutoPriceForHedge = True
        hedgeChildOrder.hedgeParam = 1
        hedgeChildOrder.parentId = parentOrder.orderId
        hedgeChildOrder.transmit = True
        ###################################### Executions ###################################################
        
        self.placeOrder(parentOrder.orderId, parent, parentOrder)
        time.sleep(1)
        self.placeOrder(hedgeChildOrder.orderId, hedgeChild, hedgeChildOrder)

        ###################################### Modifications ###################################################
        # time.sleep(2)
        # parentOrder.transmit = True
        # parentOrder.lmtPrice = 3.38

        # hedgeChildOrder.lmtPrice = 0.24

        # ###################################### Executions ###################################################
        
        # self.placeOrder(parentOrder.orderId, parent, parentOrder)
        # self.placeOrder(hedgeChildOrder.orderId, hedgeChild, hedgeChildOrder)

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
