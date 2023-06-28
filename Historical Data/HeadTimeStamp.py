from ibapi.client import *
from ibapi.common import HistogramData
from ibapi.wrapper import *
from datetime import datetime
from threading import Thread
import time
port = 7496

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        
        mycontract = Contract()

        mycontract.symbol = "AAPL"
        mycontract.secType = "STK"
        mycontract.exchange = "SMART"
        mycontract.currency = "USD"

        self.reqHeadTimeStamp(1, mycontract, "TRADES", 1, 1)
        # self.reqHeadTimeStamp(1, mycontract, "TRADES", 1, 2)

    def headTimestamp(self, reqId: int, headTimestamp: str):
        print(reqId, headTimestamp)
        self.cancelHeadTimeStamp(reqId)
        
app = TestApp()
app.connect("127.0.0.1", port, 999)
app.run()