from ibapi.client import *
from ibapi.common import HistogramData, TickerId
from ibapi.wrapper import *
from datetime import datetime
from threading import Thread
import time
port = 7496

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        
        self.orderId = orderId

        mycontract = Contract()
        mycontract.conId = 265598
        mycontract.exchange = "SMART"
        self.reqHeadTimeStamp(self.nextId(), mycontract, "MIDPOINT", 1, 1)
    
    def nextId(self):
        self.orderId += 1
        return self.orderId

    def headTimestamp(self, reqId: int, headTimestamp):
        # print(reqId, headTimestamp)
        # print(datetime.fromtimestamp(int(headTimestamp)))
        print(f"This is request attempt: {reqId}")

        self.cancelHeadTimeStamp(reqId)
        
        time.sleep(1.5)

        mycontract = Contract()
        mycontract.conId = 265598
        mycontract.exchange = "SMART"
        self.reqHeadTimeStamp(self.nextId(), mycontract, "MIDPOINT", 1, 1)

    def error(self, reqId: int, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(reqId, errorCode, errorString, advancedOrderRejectJson)
        
app = TestApp()
app.connect("127.0.0.1", port, 999)
app.run()