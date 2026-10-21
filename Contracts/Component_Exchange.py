from ibapi.client import *
from ibapi.common import SmartComponentMap
from ibapi.wrapper import *


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        self.reqSmartComponents(orderId, "9c")

    def smartComponents(self, reqId: int, smartComponentMap: SmartComponentMap):
        for i in smartComponentMap:
            print(f"Exchange: {smartComponentMap[i][0]}, Exchange Letter: {smartComponentMap[i][1]}")

    def error(self, reqId: TickerId, errorTime: int, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(f"Error., Time of Error: {errorTime}, Error Code: {errorCode}, Error Message: {errorString}")
        if advancedOrderRejectJson != "":
            print(f"AdvancedOrderRejectJson: {advancedOrderRejectJson}")

app = TestApp()
app.connect(host="127.0.0.1", port=7497, clientId=0)
app.run()