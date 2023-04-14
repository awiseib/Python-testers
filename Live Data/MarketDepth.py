from decimal import Decimal
from ibapi.client import *
from ibapi.wrapper import *
from datetime import datetime

port = 7496


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)
    
    def nextValidId(self, orderId: OrderId):

        mycontract = Contract()
        mycontract.symbol = "CMF"
        mycontract.secType = "STK"
        # mycontract.conId = 515416607
        mycontract.exchange = "SMART"
        mycontract.currency = "USD"
        # mycontract.lastTradeDateOrContractMonth = "20230224"

        self.reqMktDepth(
            reqId=12345,
            contract=mycontract,
            numRows=5,
            isSmartDepth=True,
            mktDepthOptions=[]
        )

    def updateMktDepth(
        self,
        reqId: TickerId,
        position: int,
        operation: int,
        side: int,
        price: float,
        size: Decimal,
    ):
        print(datetime.now().strftime("%H:%M:%S.%f")[:-3],
        "updateMktDepth.",
        f"reqId:{reqId}",
        f"position:{position}",
        f"operation:{operation}",
        f"side:{side}",
        f"price:{price}",
        f"size:{size}",)

    def updateMktDepthL2(
        self,
        reqId: TickerId,
        position: int,
        marketMaker: str,
        operation: int,
        side: int,
        price: float,
        size: Decimal,
        isSmartDepth: bool,
    ):print(datetime.now().strftime("%H:%M:%S.%f")[:-3],
        "updateMktDepth L2.",
        f"reqId:{reqId}",
        f"position:{position}",
        f"marketMaker {marketMaker}",
        f"operation:{operation}",
        f"side:{side}",
        f"price:{price}",
        f"size:{size}",)


app = TestApp()
app.connect("127.0.0.1", port, 1001)
app.run()
