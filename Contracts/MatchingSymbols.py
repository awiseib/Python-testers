from ibapi.client import *
from ibapi.wrapper import *

port = 7496

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        
        self.reqMatchingSymbols(orderId, "Apple")
    
    def symbolSamples(self, reqId: int, contractDescriptions: list):
        for contractDescription in contractDescriptions:
            attrs = vars(contractDescription)
            print("\n".join(f"{name}: {value}" for name, value in attrs.items()))
        
app = TestApp()
app.connect("127.0.0.1", port, 1001)
app.run()