from ibapi.client import *
from ibapi.wrapper import *


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        mktRules = [26]         # Any market rule may be added, or a list of them if a smart routed contract returns multiple.
        for i in mktRules:
            self.reqMarketRule(
                marketRuleId=i
            )

    def marketRule(self, marketRuleId: int, priceIncrements: ListOfPriceIncrements):
        print(f"marketRuleId: {marketRuleId}")
        for i in priceIncrements:
            print(i)

    def error(self, reqId: TickerId, errorTime: int, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(f"Error., Time of Error: {errorTime}, Error Code: {errorCode}, Error Message: {errorString}")
        if advancedOrderRejectJson != "":
            print(f"AdvancedOrderRejectJson: {advancedOrderRejectJson}")


app = TestApp()
app.connect(host="127.0.0.1", port=7497, clientId=0)
app.run()