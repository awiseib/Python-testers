from ibapi.client import *
from ibapi.wrapper import *


port = 7497


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):

        self.reqHistoricalNews(
            reqId=orderId, 
            conId=281858120, # BTC ConId
            providerCodes="DJ-N", #BRFG+BRFUPDN+DJNL 
            startDateTime="20250801 00:00:01", 
            endDateTime="", 
            totalResults= 15, 
            historicalNewsOptions=[]
        )     

    # Receives Data from reqHistoricalNews
    def historicalNews(self, requestId: int, time: str, providerCode: str, articleId: str, headline: str):
        print(requestId, time, providerCode, articleId, headline)

    def historicalNewsEnd(self, requestId: int, hasMore: bool):
        print(requestId, "There is no data left.")
        self.disconnect()

    def error(self, reqId: TickerId, errorTime: int, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(f"Error., Time of Error: {errorTime}, Error Code: {errorCode}, Error Message: {errorString}")
        if advancedOrderRejectJson != "":
            print(f"AdvancedOrderRejectJson: {advancedOrderRejectJson}")

app = TestApp()
app.connect("127.0.0.1", port, 0)
app.run()
