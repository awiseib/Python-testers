from decimal import Decimal
from ibapi.client import *
from ibapi.wrapper import *
from ibapi.tag_value import *
from datetime import datetime

port = 7496
global FILEPATH
FILEPATH = "C:\\Users\\awise\\Desktop\\liveBars.txt"

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):

        mycontract = Contract()
        mycontract.conId = 603764750
        mycontract.exchange = "SMART"


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
        details = f"{reqId}, {datetime.fromtimestamp(time)}, {open_}, {high}, {low}, {close}, {volume}, {wap}, {count} \n"
        liveData = open(FILEPATH, "a")
        liveData.write(details)
        liveData.close()


app = TestApp()
app.connect("127.0.0.1", port, 1001)
app.run()
