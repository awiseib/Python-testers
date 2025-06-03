from decimal import Decimal
from ibapi.client import *
from ibapi.contract import Contract
from ibapi.wrapper import *
from ibapi.contract import *

port = 7496

class TestApp(EWrapper, EClient):

    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: int):
        self.reqPositions()

    def position(self, account: str, contract: Contract, position: Decimal, avgCost: float):
        # print(f"Positions. Account: {account}, Contract: {contract}, Position: {position}, Average Cost: {avgCost}")
        print(f"{contract.symbol} | {contract.secType} | PrimaryExchange: {contract.primaryExchange} | Exchange: {contract.exchange}")

    def positionEnd(self):
        self.cancelPositions()
        print("End of positions")

    def error(self, reqId: TickerId, errorTime: int, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(f"Error., Time of Error: {errorTime}, Error Code: {errorCode}, Error Message: {errorString}")
        if advancedOrderRejectJson != "":
            print(f"AdvancedOrderRejectJson: {advancedOrderRejectJson}")

    
app = TestApp()
app.connect('127.0.0.1', port, 0)
app.run()