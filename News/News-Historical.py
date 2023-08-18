from ibapi.client import *
from ibapi.wrapper import *
from datetime import datetime


port = 7496


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):

        # Returns your subscribed news sources via newsProviders callback.
        # self.reqNewsProviders()

        self.reqHistoricalNews(
            reqId=1234, 
            conId=265598, # AAPL ConId
            providerCodes="BRFG+BRFUPDN+DJNL", #BRFG+BRFUPDN+DJNL 
            startDateTime="", 
            endDateTime="20230814-12:00:00", 
            totalResults= 10, 
            historicalNewsOptions=[]
        )

    # Receives Data from reqHistoricalNews
    def historicalNews(self, requestId: int, time: str, providerCode: str, articleId: str, headline: str):
        print(requestId, time, providerCode, articleId, headline)

app = TestApp()
app.connect("127.0.0.1", port, 1001)
app.run()
