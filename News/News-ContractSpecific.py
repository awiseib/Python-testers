from ibapi.client import *
from ibapi.wrapper import *
from ibapi.tag_value import *
from ibapi.ticktype import TickTypeEnum

port = 7497


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: int):
        # Creates a contract specific news source and denotes the news feed through 'genericTickList="mdoff,292:BRFG"'.

        contract = Contract()
        # contract.conId = 265598 # AAPL ConId
        contract.symbol = "B4B"
        contract.currency = "EUR"
        contract.secType = "STK"
        contract.exchange = "VALUE"

        # Places the request for news data. Note the generic tick list string.
        self.reqMktData(orderId, contract,"mdoff,292:DJ-N", False, False, [])


    def tickNews(self, tickerId: int, timeStamp: int, providerCode: str, articleId: str, headline: str, extraData: str):
        print(f"tickNews. tickerId:{tickerId}, timeStamp:{timeStamp}, providerCode:{providerCode}, articleId:{articleId}, headline:{headline}, extraData:{extraData}")

    def tickString(self, reqId: TickerId, tickType: TickType, value: str):
        print(f"tickString. ID: {reqId}, tickType: {TickTypeEnum.toStr(tickType)}, Value: {value}")

app = TestApp()
app.connect("127.0.0.1", port, 0)
app.run()

