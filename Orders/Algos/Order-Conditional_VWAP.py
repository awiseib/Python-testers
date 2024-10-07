from decimal import Decimal
from ibapi.tag_value import TagValue
from ibapi.client import *
from ibapi.wrapper import *
from datetime import datetime
import ibapi.order_condition as oc

port = 7496


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        contract = Contract()
        contract.conId = 8894
        contract.symbol = "KO"
        contract.secType = "STK"
        contract.exchange = "SMART"
        contract.currency = "USD"
        
        order = Order()
        order.action = "BUY"
        order.totalQuantity = 100
        order.orderType = "MKT"
        order.tif = "DAY"
        order.algoStrategy = "AD"


        order.algoStrategy = "AD"
        order.algoParams = []
        order.algoParams.append(TagValue("componentSize", 100))
        order.algoParams.append(TagValue("timeBetweenOrders", 1))
        order.algoParams.append(TagValue("randomizeTime20", int(1)))
        order.algoParams.append(TagValue("randomizeSize55", int(1)))
        order.algoParams.append(TagValue("giveUp", 0))
        order.algoParams.append(TagValue("catchUp", int(1)))
        order.algoParams.append(TagValue("waitForFill", int(0)))
        
        # order.conditions = [
        #     oc.OperatorCondition(

        #     )
        # ]


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
            f"\nAlgo: {order.algoStrategy}",
            f"\nAlgo Params: {order.algoParams}",
            f"\nConditions: {order.conditions}",
            f"\nMisc Options: {order.orderMiscOptions}"
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
app.connect("127.0.0.1", port, 0)
app.run()

