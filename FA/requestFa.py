from ibapi.client import *
from ibapi.wrapper import *
from ibapi.common import *

port = 7496

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        self.requestFA(FaDataTypeEnum.GROUPS)

    def receiveFA(self, faData: FaDataType, cxml: str):
        print(faData, cxml)

    def error(self, reqId: TickerId, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(reqId, errorCode, errorString, advancedOrderRejectJson)
        
app = TestApp()
app.connect("127.0.0.1", port, 999)
app.run()