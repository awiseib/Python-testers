from ibapi.client import *
from ibapi.wrapper import *



class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        self.reqPnLSingle(
            reqId=orderId, 
            account="U1234567", # The accountId is always required, even if only one account is availble. 
            modelCode="",        # Should be left as a blank string unless logged in as an Advisor.
            conid=265598
        )

    def pnlSingle(self, reqId: int, pos: Decimal, dailyPnL: float, unrealizedPnL: float, realizedPnL: float, value: float):
        print(f"pnlSingle. pos: {pos}, dailyPnL: {dailyPnL}, unrealizedPnL: {round(unrealizedPnL,2)}, realizedPnL: {round(realizedPnL,2)}, value: {round(value,2)}")

    def error(self, reqId: TickerId, errorTime: int, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(f"Error., Time of Error: {errorTime} Error Code: {errorCode}, Error Message: {errorString}")
        if advancedOrderRejectJson != "":
            print(f"AdvancedOrderRejectJson: {advancedOrderRejectJson}")
        
app = TestApp()
app.connect(host="127.0.0.1", port=7497, clientId=0)
app.run()