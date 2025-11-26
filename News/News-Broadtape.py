from ibapi.client import *
from ibapi.wrapper import *
from ibapi.tag_value import *
from ibapi.ticktype import TickTypeEnum

port = 7496


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: int):
        # Creates a generic feed that provides all news articles sent by the resource
        # Must set generic tick list to 'genericTickList="mdoff,292"' when using this request.
        contract2 = Contract()
        # contract2.symbol = "BZ:BZ_ALL"
        contract2.symbol = "DJ:N_RBS"
        contract2.secType = "NEWS"
        contract2.exchange = "DJ"

        # Places the request for news data. Note the generic tick list string.
        self.reqMktData(
            reqId=orderId,
            contract=contract2,
            genericTickList="mdoff,292",
            snapshot=False,
            regulatorySnapshot=False,
            mktDataOptions=[],
        )

    # Only the necessary news-related callbacks are implemented below

    # Headlines delivered to this callback after reqMktData for broadtape news
    def tickNews(self, tickerId: int, timeStamp: int, providerCode: str, articleId: str, headline: str, extraData: str):
        print(f"tickNews. tickerId:{tickerId}, timeStamp:{timeStamp}, providerCode:{providerCode}, articleId:{articleId}, headline:{headline}, extraData:{extraData}")

    def tickString(self, reqId: TickerId, tickType: TickType, value: str):
        print(f"tickString. ID: {reqId}, tickType: {TickTypeEnum.toStr(tickType)}, Value: {value}")

    def error(self, reqId: TickerId, errorTime: int, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(f"Error., Time of Error: {errorTime}, Error Code: {errorCode}, Error Message: {errorString}")
        if advancedOrderRejectJson != "":
            print(f"AdvancedOrderRejectJson: {advancedOrderRejectJson}")

app = TestApp()
app.connect("127.0.0.1", port, 0)
app.run()