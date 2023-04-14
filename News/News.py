from ibapi.client import *
from ibapi.wrapper import *

# Change as necessary
port = 7496


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):

        # Creates a contract specific news source and denotes the news feed through 'genericTickList="mdoff,292:BRFG"'.
        mycontract = Contract()
        mycontract.symbol="TSLA"
        mycontract.secType="STK"
        mycontract.exchange="SMART"
        mycontract.currency="USD"

        # Creates a generic feed that provides all news articles sent by the resource
        # Must set generic tick list to 'genericTickList="mdoff,292"' when using this request.
        contract2 = Contract()
        contract2.symbol = "DJNL:DJNL_ALL"
        contract2.secType = "NEWS"
        contract2.exchange = "DJNL"

        # Places the request for news data. Note the generic tick list string.
        self.reqMktData(
            reqId=123,
            contract=mycontract,
            genericTickList="mdoff,292:BRFUPDN",
            snapshot=False,
            regulatorySnapshot=False,
            mktDataOptions=[],
        )

    # Only the necessary news-related callbacks are implemented below

    # Headlines delivered to this callback after reqMktData for broadtape news
    def tickNews(
        self,
        tickerId: int,
        timeStamp: int,
        providerCode: str,
        articleId: str,
        headline: str,
        extraData: str,
    ):
        print(
            "tickNews.",
            f"tickerId:{tickerId}",
            f"timeStamp:{timeStamp}",
            f"providerCode:{providerCode}",
            f"articleId:{articleId}",
            f"headline:{headline}",
            f"extraData:{extraData}",
        )

    def tickString(self, reqId: TickerId, tickType: TickType, value: str):
        print(reqId, tickType, value)

    # Subscribed news sources are delivered here after reqNewsProviders
    def newsProviders(self, newsProviders: ListOfNewsProviders):
        print(
            "newsProviders.",
            f"newsProviders:{newsProviders}",
        )

app = TestApp()
app.connect("127.0.0.1", port, 1001)
app.run()
