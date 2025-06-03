from ibapi.client import *
from ibapi.wrapper import *
from ibapi.account_summary_tags import *

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: int):
        self.reqAccountUpdatesMulti(orderId, "DU74649", "", False)

    def updateAccountValue(
        self, key: str, val: str, currency: str, accountName: str
    ):
        print("updateAccountValue.", key, val, currency, accountName)

    def updateAccountTime(self, timeStamp: str):
        print("updateAccountTime.", timeStamp)

    def updatePortfolio(self, contract: Contract, position: Decimal, marketPrice: float, marketValue: float, averageCost: float, unrealizedPNL: float, realizedPNL: float, accountName: str):
        print(f"updatePortfolio. contract: {contract.symbol}@{contract.exchange}:{contract.secType}, position: {position}, marketPrice: {marketPrice}, marketValue: {marketValue}, averageCost: {averageCost}, unrealizedPNL: {unrealizedPNL}, realizedPNL: {realizedPNL}")

    def accountDownloadEnd(self, accountName: str):
        print("accountDownloadEnd.", accountName)
        self.disconnect()

    def error(self, reqId: TickerId, errorTime: int, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(f"Error., Time of Error: {errorTime}, Error Code: {errorCode}, Error Message: {errorString}")
        if advancedOrderRejectJson != "":
            print(f"AdvancedOrderRejectJson: {advancedOrderRejectJson}")
            
app = TestApp()
app.connect("127.0.0.1", 7496, 1001)
app.run()
