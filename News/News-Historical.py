from ibapi.client import *
from ibapi.wrapper import *
from datetime import datetime


port = 7496


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):

        self.reqHistoricalNews(
            reqId=orderId, 
            conId=8314, # AAPL ConId
            providerCodes="BRFG+BRFUPDN+DJNL", #BRFG+BRFUPDN+DJNL 
            startDateTime="20200101 00:00:01", 
            endDateTime="", 
            totalResults= 300, 
            historicalNewsOptions=[]
        )

    # Receives Data from reqHistoricalNews
    def historicalNews(self, requestId: int, time: str, providerCode: str, articleId: str, headline: str):
        print(requestId, time, providerCode, articleId, headline)

    def historicalNewsEnd(self, requestId: int, hasMore: bool):
        print(requestId, hasMore)
        self.disconnect()

app = TestApp()
app.connect("127.0.0.1", port, 1001)
app.run()
