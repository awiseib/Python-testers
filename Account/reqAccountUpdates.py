from decimal import Decimal
from ibapi.client import *
from ibapi.wrapper import *

port = 7496

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        print(f"nextValidId. orderId={orderId}")

        self.reqAccountUpdates(True, "DU5240685")

    def updateAccountValue(
        self, key: str, val: str, currency: str, accountName: str
    ):
        print("updateAccountValue.", key, val, currency, accountName)

    # def updateAccountTime(self, timeStamp: str):
    #     print("updateAccountTime.", timeStamp)

    def updatePortfolio(self, contract: Contract, position: Decimal, marketPrice: float, marketValue: float, averageCost: float, unrealizedPNL: float, realizedPNL: float, accountName: str):
        print(f"updatePortfolio. contract: {contract.symbol}@{contract.exchange}:{contract.secType}, position: {position}, marketPrice: {marketPrice}, marketValue: {marketValue}, averageCost: {averageCost}, unrealizedPNL: {unrealizedPNL}, realizedPNL: {realizedPNL}")

    def accountDownloadEnd(self, accountName: str):
        print("accountDownloadEnd.", accountName)
        # self.disconnect()


app = TestApp()
app.connect("127.0.0.1", port, 1001)
app.run()
