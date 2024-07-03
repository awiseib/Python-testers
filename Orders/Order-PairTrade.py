from decimal import Decimal
from ibapi.client import *
from ibapi.wrapper import *
from ibapi.contract import *
import time

port = 7496

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        print(f"nextValidId. orderId={orderId}")

        ###################################### Contracts ###################################################
        parent = Contract()
        parent.conId = 29831612      #DPZ (Domino's Pizza)
        parent.exchange = "SMART"

        hedgeChild = Contract()
        hedgeChild.conId = 273538    #PZZA (Papa John's)
        hedgeChild.exchange = "SMART"
        
        ###################################### Parent Order ###################################################
        parentOrder = Order()
        parentOrder.orderId = orderId
        parentOrder.action = "BUY"
        parentOrder.orderType = "MKT"
        #parentOrder.orderType = "LMT"
        #parentOrder.lmtPrice = 515
        
        parentOrder.totalQuantity = 1
        parentOrder.transmit = False
        #parentOrder.account = ""
        ###################################### Hedged Child Order ###################################################
        hedgeChildOrder = Order()
        hedgeChildOrder.orderId = orderId + 1
        hedgeChildOrder.parentId = orderId
        hedgeChildOrder.action = "SELL"
        hedgeChildOrder.orderType = "MKT"
        hedgeChildOrder.totalQuantity = 0
        hedgeChildOrder.hedgeType = "P"        #P for Pair Trade
        hedgeChildOrder.hedgeParam = 5         #Hedge Ratio
        hedgeChildOrder.transmit = True
        #hedgeChildOrder.account = ""
        ###################################### Executions ###################################################
        
        self.placeOrder(parentOrder.orderId, parent, parentOrder)
        time.sleep(.2)
        self.placeOrder(hedgeChildOrder.orderId, hedgeChild, hedgeChildOrder)


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

    # def error(
    #     self,
    #     reqId: TickerId,
    #     errorCode: int,
    #     errorString: str,
    #     advancedOrderRejectJson="",
    # ):
    #     print(
    #         datetime.now().strftime("%H:%M:%S.%f")[:-3],
    #         "error.",
    #         f"reqId:{reqId}",
    #         f"errorCode:{errorCode}",
    #         f"errorString:{errorString}",
    #         f"advancedOrderRejectJson:{advancedOrderRejectJson}",
    #     )

app = TestApp()
app.connect("127.0.0.1", port, 1001)
app.run()