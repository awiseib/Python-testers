from decimal import Decimal
from ibapi.client import *
from ibapi.wrapper import *

port = 7497


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        self.requestFA(FaDataTypeEnum.GROUPS)

    def receiveFA(self, faData: FaDataType, cxml: str):
        print(cxml)

    # def error(self, reqId: TickerId, errorCode: int, errorString: str):
    #     print(f"error. reqId:{reqId} code:{errorCode} string:{errorString}")


app = TestApp()
app.connect("127.0.0.1", port, 1001)
app.run()
