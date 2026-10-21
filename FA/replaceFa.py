from ibapi.client import *
from ibapi.wrapper import *
from ibapi.common import *


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        faData = open(r"C:\Users\awise\Code\Python testers\FA\faData_Groups.xml", "r")
        self.replaceFA(orderId, 1 , faData.read())

    def replaceFAEnd(self, reqId: int, text: str):
        print("Request End", text)
        self.disconnect()

    def error(self, reqId: TickerId, errorTime: int, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(f"Error., Time of Error: {errorTime}, Error Code: {errorCode}, Error Message: {errorString}")
        if advancedOrderRejectJson != "":
            print(f"AdvancedOrderRejectJson: {advancedOrderRejectJson}")
        
app = TestApp()
app.connect(host="127.0.0.1", port=7497, clientId=0)
app.run()