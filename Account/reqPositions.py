from ibapi.client import *
from ibapi.wrapper import *
from ibapi.contract import *
import time
import threading

port = 7496

class TestApp(EWrapper, EClient):

    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: int):
        self.reqPositions()

    def position(self, account: str, contract: Contract, position: Decimal, avgCost: float):
        print(account, contract, position, avgCost)

    def positionEnd(self):
        self.cancelPositions()
        print("End of positions")

    def error(self, reqId: TickerId, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print("Error.", errorCode, errorString, advancedOrderRejectJson)

    
app = TestApp()
app.connect('127.0.0.1', port, 0)
app.run()