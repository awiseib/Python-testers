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
        
app = TestApp()
app.connect("127.0.0.1", port, 999)
app.run()