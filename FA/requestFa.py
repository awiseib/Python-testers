from ibapi.common import FaDataType,FaDataTypeEnum
from ibapi.client import *
from ibapi.wrapper import *



class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        self.requestFA(FaDataTypeEnum.GROUPS)

    def receiveFA(self, faData: FaDataType, cxml: str):
        print(cxml)

    def error(self, reqId: TickerId, errorTime: int, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(f"Error., Time of Error: {errorTime}, Error Code: {errorCode}, Error Message: {errorString}")
        if advancedOrderRejectJson != "":
            print(f"AdvancedOrderRejectJson: {advancedOrderRejectJson}")


app = TestApp()
app.connect(host="127.0.0.1", port=7497, clientId=0)
app.run()
