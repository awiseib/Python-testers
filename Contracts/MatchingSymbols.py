from ibapi.client import *
from ibapi.wrapper import *


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        
        self.reqMatchingSymbols(
            reqId=orderId, 
            pattern="IB" # This functions identical to the TWS contract lookup tool when seeking contracts from the watchlist.
        )
    
    def symbolSamples(self, reqId: int, contractDescriptions: list):
        for contractDescription in contractDescriptions:
            attrs = vars(contractDescription)
            print("\n".join(f"{name}: {value}" for name, value in attrs.items()))
            print()

    def error(self, reqId: TickerId, errorTime: int, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(f"Error., Time of Error: {errorTime}, Error Code: {errorCode}, Error Message: {errorString}")
        if advancedOrderRejectJson != "":
            print(f"AdvancedOrderRejectJson: {advancedOrderRejectJson}")

app = TestApp()
app.connect(host="127.0.0.1", port=7497, clientId=0)
app.run()