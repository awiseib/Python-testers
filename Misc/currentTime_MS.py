from ibapi.client import *
from ibapi.wrapper import *
import datetime

port = 7496


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        self.reqCurrentTimeInMillis()

    def currentTimeInMillis(self, timeInMillis: int):
        print(timeInMillis)

    def error(self, reqId: TickerId, et, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(reqId, errorCode, errorString, advancedOrderRejectJson)


app = TestApp()
app.connect("127.0.0.1", port, 0)
app.run()