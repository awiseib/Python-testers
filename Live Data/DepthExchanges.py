from ibapi.client import *
from ibapi.wrapper import *

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)
        
    def nextValidId(self, orderId):
        self.reqMktDepthExchanges()

    def mktDepthExchanges(self, depthMktDataDescriptions):
        for deepExchange in depthMktDataDescriptions:
            print(f"Exchange: {deepExchange.exchange}, SecType: {deepExchange.secType}, ListingExchange: {deepExchange.listingExch}, ServiceDataType: {deepExchange.serviceDataType}, AggGroup: {deepExchange.aggGroup}")

    def error(self, reqId: TickerId, errorTime: int, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(f"Error., Time of Error: {errorTime}, Error Code: {errorCode}, Error Message: {errorString}")
        if advancedOrderRejectJson != "":
            print(f"AdvancedOrderRejectJson: {advancedOrderRejectJson}")
        

app = TestApp()
app.connect(host="127.0.0.1", port=7497, clientId=0)
app.run()