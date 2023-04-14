from ibapi.client import *
from ibapi.wrapper import *
from threading import Thread
port = 7496


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        mktRules = [557]
        for i in mktRules:
            Thread(target=self.reqMarketRule(i)).start()

    def marketRule(self, marketRuleId: int, priceIncrements: ListOfPriceIncrements):
        print(f"marketRuleId: {marketRuleId}")
        for i in priceIncrements:
            print(i)


app = TestApp()
app.connect("127.0.0.1", port, 1005)
app.run()