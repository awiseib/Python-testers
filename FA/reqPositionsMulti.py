from ibapi.client import *
from ibapi.contract import Contract
from ibapi.utils import Decimal
from ibapi.wrapper import *
from ibapi.contract import *
import time
import threading

port = 7496

class TestApp(EWrapper, EClient):

    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: int):
        self.reqPositionsMulti(orderId, "DU5240685", "")

    def positionMulti(self, reqId: int, account: str, modelCode: str, contract: Contract, pos: Decimal, avgCost: float):
        print(f"reqId: {reqId}, account: {account}, modelCode: {modelCode}, contract: {contract}, pos: {pos}, avgCost: {avgCost}")
    
    def cancelPositionsMulti(self, reqId: int):
        self.cancelPositionsMulti(reqId)

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