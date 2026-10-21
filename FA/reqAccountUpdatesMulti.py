from ibapi.client import *
from ibapi.wrapper import *



class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        self.reqAccountUpdatesMulti(
            reqId=orderId, 
            account="DU5240685", 
            modelCode="", 
            ledgerAndNLV=False # Declare if Ledger and Net Liquidation values should be returned.
        )

    def accountUpdateMulti(self, reqId: TickerId, account: str, modelCode: str, key: str, value: str, currency: str):
        print("updateAccountValue.", key, value, currency, account)
    
    def accountUpdateMultiEnd(self, reqId: TickerId):
        print("End of "+str(reqId))

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

if __name__ == "__main__":
    app = TestApp()
    app.connect(host="127.0.0.1", port=7497, clientId=0)
    app.run()