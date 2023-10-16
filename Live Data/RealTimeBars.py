from decimal import Decimal
from ibapi.client import *
from ibapi.wrapper import *
from ibapi.tag_value import *
from datetime import datetime

port = 7496


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):

        mycontract = Contract()
        mycontract.symbol = "K"
        mycontract.secType = "STK"
        mycontract.exchange = "SMART"
        mycontract.currency = "USD"


        self.reqRealTimeBars(
            reqId=123,
            contract=mycontract,
            barSize=5,
            whatToShow="TRADES",
            useRTH=False,
            realTimeBarsOptions=[],
        )

    def realtimeBar(
        self,
        reqId: TickerId,
        time: int,
        open_: float,
        high: float,
        low: float,
        close: float,
        volume: Decimal,
        wap: Decimal,
        count: int,
    ):
        print(
            datetime.now().strftime("%H:%M:%S.%f")[:-3],
            "realtimeBar.",
            f"reqId:{reqId}",
            f"time:{time}",
            f"open_:{open_}",
            f"high:{high}",
            f"low:{low}",
            f"close:{close}",
            f"volume:{volume}",
            f"wap:{wap}",
            f"count:{count}",
        )

    def error(self, reqId: TickerId, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(reqId, errorCode, errorString, advancedOrderRejectJson)


app = TestApp()
app.connect("127.0.0.1", port, 1001)
app.run()
