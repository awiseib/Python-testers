from ibapi.client import *
from ibapi.wrapper import *
import ibapi.order_condition as oc

port = 7496


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        print(f"nextValidId. orderId={orderId}")

        # price_condition = oc.Create(oc.OrderCondition.Price)
        # price_condition.conId = 4391
        # price_condition.exchange = "ISLAND"
        # price_condition.isMore = True
        # price_condition.triggerMethod = 2 # Last price trigger
        # price_condition.price = 133
        # price_condition.isConjunctionConnection = True # True = And, False = Or

        # volume_condition = oc.Create(oc.OrderCondition.Volume)
        # volume_condition.conId = 4391 # AMD
        # volume_condition.exchange = "ISLAND"
        # volume_condition.isMore = True
        # volume_condition.volume = 5000
        # volume_condition.isConjunctionConnection = True # And

        # time_condition = oc.Create(oc.OrderCondition.Time)
        # time_condition.isMore = True # After
        # time_condition.time = "20230610 12:00:00 "
        # time_condition.isConjunctionConnection = True # And

        # percent_condition = oc.Create(oc.OrderCondition.PercentChange)
        # percent_condition.conId = 272093 # MSFT
        # percent_condition.exchange = "ISLAND"
        # percent_condition.isMore = True
        # percent_condition.changePercent = 3.0
        # percent_condition.isConjunctionConnection = True
        
        conditions = [
            # oc.VolumeCondition(
            #     conId=8314, 
            #     exch="SMART", 
            #     isMore=True, 
            #     volume=1000000
            # ).And(),
            # oc.PercentChangeCondition(
            #     conId=4391, 
            #     exch="ISLAND", 
            #     isMore=True, 
            #     changePercent=0.25
            # ).Or(),
            # oc.PriceCondition(
            #     triggerMethod=2,
            #     conId=4391,
            #     exch="SMART",
            #     isMore=False,
            #     price=120,
            # )
            # .And(),
            # oc.TimeCondition(
            #     isMore=True, 
            #     time="20170101 09:30:00"
            # ).And(),
            # oc.MarginCondition(
            #     isMore=False, 
            #     percent=20 # percent within a range of (0, 100)
            # ).Or(),
            # oc.ExecutionCondition(
            #     secType="STK", 
            #     exch="SMART", 
            #     symbol="AMD"
            # )
        ]

        mycontract = Contract()
        mycontract.symbol = "SPY"
        mycontract.secType = "STK"
        mycontract.exchange = "SMART"
        mycontract.currency = "USD"

        myorder = Order()
        myorder.orderId = orderId
        myorder.action = "BUY"
        myorder.orderType = "LMT"
        myorder.totalQuantity = 1
        myorder.lmtPrice = 409.00
        myorder.tif = "GTC"
        myorder.outsideRth = True
        myorder.conditions.append(
            oc.TimeCondition(
                isMore=True, 
                time="12:00:00 America/Chicago"
            ))
        # for c in conditions:
        #     myorder.conditions.append(c)
        myorder.conditionsCancelOrder 
        self.placeOrder(orderId, mycontract, myorder)

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


app = TestApp()
app.connect("127.0.0.1", port, 1001)
app.run()
