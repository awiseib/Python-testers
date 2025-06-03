from decimal import Decimal
from ibapi.client import *
from ibapi.wrapper import *



class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        self.reqPnLSingle(orderId, "DU5240685", "", 265598) # This request will check my account's AAPL position.

    def pnlSingle(self, reqId: int, pos: Decimal, dailyPnL: float, unrealizedPnL: float, realizedPnL: float, value: float):
        print(f"pnlSingle. pos: {pos}, dailyPnL: {dailyPnL}, unrealizedPnL: {round(unrealizedPnL,2)}, realizedPnL: {round(realizedPnL,2)}, value: {round(value,2)}")

    def error(self, reqId: TickerId, errorTime: int, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(f"Error., Time of Error: {errorTime} Error Code: {errorCode}, Error Message: {errorString}")
        if advancedOrderRejectJson != "":
            print(f"AdvancedOrderRejectJson: {advancedOrderRejectJson}")
        
app = TestApp()
app.connect("127.0.0.1", 7496, 1002)
app.run()