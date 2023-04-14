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
            providerCodes="BRFG+BRFUPDN", #BRFG+BRFUPDN+DJNL 
            startDateTime="", 
            endDateTime="0-12-00 00:00:00", 
            totalResults= 1, 
            historicalNewsOptions=[]
        )

    # Receives Data from reqHistoricalNews
    def historicalNews(self, requestId: int, time: str, providerCode: str, articleId: str, headline: str):
        print(requestId, time, providerCode, articleId, headline)

    # Subscribed news sources are delivered here after reqNewsProviders
    def newsProviders(self, newsProviders: ListOfNewsProviders):
        print(
            "newsProviders.",
            f"newsProviders:{newsProviders}",
        )

    def error(
        self,
        reqId: TickerId,
        errorCode: int,
        errorString: str,
        advancedOrderRejectJson="",
    ):
        print(
            datetime.now().strftime("%H:%M:%S.%f")[:-3],
            "error.",
            f"reqId:{reqId}",
            f"errorCode:{errorCode}",
            f"errorString:{errorString}",
            f"advancedOrderRejectJson:{advancedOrderRejectJson}",
        )


app = TestApp()
app.connect("127.0.0.1", port, 1001)
app.run()
