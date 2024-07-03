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

        mycontract = Contract()
        mycontract.conId = 8314 # IBM STK
        mycontract.exchange = "SMART"
        mycontract.currency = "USD"

        myorder = Order()
        myorder.orderId = orderId
        myorder.orderType = "PEG BENCH"
        # BUY or SELL
        myorder.action = "BUY"
        myorder.totalQuantity = 100
        #Beginning with price...
        myorder.startingPrice = 0
        #increase/decrease price..
        myorder.isPeggedChangeAmountDecrease = False
        #by... (and likewise for price moving in opposite direction)
        myorder.peggedChangeAmount = 3
        #whenever there is a price change of...
        myorder.referenceChangeAmount = 1
        #in the reference contract...
        myorder.referenceContractId = 265598 # IGF STK
        #being traded at...
        myorder.referenceExchangeId = "SMART"
        #starting reference price is...
        myorder.stockRefPrice = 219
        #Keep myorder active as long as reference contract trades between...
        myorder.stockRangeLower = 200
        #and...
        myorder.stockRangeUpper = 220

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
        print(order.startingPrice)

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

