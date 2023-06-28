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

        self.reqHistogramData(tickerId=orderId, contract=mycontract, useRTH=True, timePeriod="3 mins")

    def histogramData(self, reqId: int, items: HistogramData):
        print(reqId, items)
        self.cancelHistogramData(reqId)
        
app = TestApp()
app.connect("127.0.0.1", port, 999)
app.run()