from ibapi.client import *
from ibapi.common import SmartComponentMap
from ibapi.wrapper import *

port = 7496

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        self.reqSmartComponents(orderId, "9c")

    def smartComponents(self, reqId: int, smartComponentMap: SmartComponentMap):
        for i in smartComponentMap:
            print(f"Exchange: {i.exchange}, Exchange Letter: {i.exchangeLetter}")
        
    def error(self, reqId: TickerId, errorTime: int, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(f"Error., Time of Error: {errorTime}, Error Code: {errorCode}, Error Message: {errorString}")
        if advancedOrderRejectJson != "":
            print(f"AdvancedOrderRejectJson: {advancedOrderRejectJson}")

app = TestApp()
app.connect("127.0.0.1", port, 0)
app.run()