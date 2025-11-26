from decimal import Decimal
from ibapi.client import *
from ibapi.common import TickerId
from ibapi.wrapper import *

port = 7496

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        self.reqAccountUpdates(True, "")

    # def updateAccountValue(
    #     self, key: str, val: str, currency: str, accountName: str):
    #     print("updateAccountValue.", key, val, currency, accountName)

    # def accountUpdateMulti(self, reqId: TickerId, account: str, modelCode: str, key: str, value: str, currency: str):
    #     print("updateAccountValue.", key, value, currency, account)
    
    # def accountUpdateMultiEnd(self, reqId: TickerId):
    #     print("End of "+str(reqId))

    # def updateAccountTime(self, timeStamp: str):
    #     print("updateAccountTime.", timeStamp)

    def updatePortfolio(self, contract: Contract, position: Decimal, marketPrice: float, marketValue: float, averageCost: float, unrealizedPNL: float, realizedPNL: float, accountName: str):
        print(f"updatePortfolio. contract: {contract.symbol}@{contract.exchange}:{contract.secType}, position: {position}, marketPrice: {marketPrice}, marketValue: {marketValue}, averageCost: {averageCost}, unrealizedPNL: {unrealizedPNL}, realizedPNL: {realizedPNL}")
    
    # def accountDownloadEnd(self, accountName: str):
    #     print("accountDownloadEnd.", accountName)
    #     self.disconnect()

    # def error(self, reqId: TickerId, errorTime: int, errorCode: int, errorString: str, advancedOrderRejectJson=""):
    #     print(f"Error., Time of Error: {errorTime}, Error Code: {errorCode}, Error Message: {errorString}")
    #     if advancedOrderRejectJson != "":
    #         print(f"AdvancedOrderRejectJson: {advancedOrderRejectJson}")


app = TestApp()
app.connect("127.0.0.1", port, 0)
app.run()