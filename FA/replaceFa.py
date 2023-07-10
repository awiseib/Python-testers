from ibapi.client import *
from ibapi.common import FaDataType, TickerId
from ibapi.wrapper import *
from ibapi.common import *
import time

port = 7496

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        faData = open("./FA/faData.xml", "r")
        self.replaceFA(orderId, FaDataTypeEnum.GROUPS, faData.read())

    def replaceFAEnd(self, reqId: int, text: str):
        print("Request End", text)

    def error(self, reqId: TickerId, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(reqId, errorCode, errorString, advancedOrderRejectJson)
        
app = TestApp()
app.connect("127.0.0.1", port, 999)
time.sleep(3)
app.run()