from ibapi.client import *
from ibapi.wrapper import *
from ibapi.tag_value import *
from ibapi.ticktype import TickTypeEnum


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: int):
        # Creates a contract specific news source and denotes the news feed through 'genericTickList="mdoff,292:BRFG"'.

        mycontract = Contract()
        mycontract.symbol = "AAPL"
        mycontract.secType = "STK"
        mycontract.exchange = "SMART"
        mycontract.currency = "USD"

        # Places the request for news data. Note the generic tick list string.
        self.reqMktData(
            reqId=orderId, 
            contract=mycontract,
            genericTickList="mdoff,292:DJ-N", 
            snapshot=False, 
            regulatorySnapshot=False, 
            mktDataOptions=[]
        )


    def tickNews(self, tickerId: int, timeStamp: int, providerCode: str, articleId: str, headline: str, extraData: str):
        print(f"tickNews. tickerId:{tickerId}, timeStamp:{timeStamp}, providerCode:{providerCode}, articleId:{articleId}, headline:{headline}, extraData:{extraData}")

    def tickString(self, reqId: TickerId, tickType: TickType, value: str):
        print(f"tickString. ID: {reqId}, tickType: {TickTypeEnum.toStr(tickType)}, Value: {value}")

    def error(self, reqId: TickerId, errorTime: int, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(f"Error., Time of Error: {errorTime}, Error Code: {errorCode}, Error Message: {errorString}")
        if advancedOrderRejectJson != "":
            print(f"AdvancedOrderRejectJson: {advancedOrderRejectJson}")

app = TestApp()
app.connect(host="127.0.0.1", port=7497, clientId=0)
app.run()

