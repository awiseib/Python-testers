from ibapi.client import *
from ibapi.wrapper import *
import time

port = 7497
clientId = 0

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: int):
        self.reqAccountUpdates(True, "DU257590")

        self.reqOpenOrders()

        contract = Contract()
        contract.localSymbol = "EUR.USD"
        contract.exchange = "IDEALPRO"
        contract.secType = "CASH"
        self.reqMktData(orderId, contract, "", 1, 0, [])

    def tickPrice(self, reqId: TickerId, tickType: TickType, price: float, attrib: TickAttrib):
        print(reqId, tickType, price, attrib)

    def tickSnapshotEnd(self, reqId: int):
        print("End of tick snapshot")
        self.cancelMktData(reqId)
    
    def openOrder(self, orderId: OrderId, contract: Contract, order: Order, orderState: OrderState):
        print(orderId, contract, order, orderState)

    def updateAccountValue(self, key: str, val: str, currency: str, accountName: str):
        print(key, val, currency, accountName)
    
    def updatePortfolio(self, contract: Contract, position: Decimal, marketPrice: float, marketValue: float, averageCost: float, unrealizedPNL: float, realizedPNL: float, accountName: str):
        print(contract, position, marketPrice, marketValue, averageCost, unrealizedPNL, realizedPNL, accountName)

    def accountDownloadEnd(self, accountName: str):
        print("End of account download")
        self.cancelPositions()
        self.disconnect()

while True:

    app = TestApp()
    app.connect("127.0.0.1", port, clientId)
    app.run()
    time.sleep(2)