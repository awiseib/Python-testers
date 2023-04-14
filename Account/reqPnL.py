from decimal import Decimal
from ibapi.client import *
from ibapi.wrapper import *

import threading


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        # self.reqPnLSingle(105468, "DU5240685", "", 265598)
        self.reqPnL(105468, "ALL", "")

    def pnlSingle(self, reqId: int, pos: Decimal, dailyPnL: float, unrealizedPnL: float, realizedPnL: float, value: float):
        print(f"pnlSingle. pos: {pos}, dailyPnL: {dailyPnL}, unrealizedPnL: {round(unrealizedPnL,2)}, realizedPnL: {round(realizedPnL,2)}, value: {round(value,2)}")

    def pnl(self, reqId: int, dailyPnL: float, unrealizedPnL: float, realizedPnL: float):
        print(f"pnl. reqId: {reqId}, dailyPnL: {dailyPnL}, unrealizedPnL: {round(unrealizedPnL,2)}, realizedPnL: {round(realizedPnL,2)}")

    def error(self, reqId: TickerId, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print("error",reqId, errorCode, errorString, advancedOrderRejectJson)
        
app = TestApp()
app.connect("127.0.0.1", 7496, 1001)
app.run()
