from decimal import Decimal
from ibapi.client import *
from ibapi.wrapper import *

import threading
import time


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def pnl(self, reqId: int, dailyPnL: float, unrealizedPnL: float, realizedPnL: float):
        print(f"pnl. reqId: {reqId}, dailyPnL: {dailyPnL}, unrealizedPnL: {round(unrealizedPnL,2)}, realizedPnL: {round(realizedPnL,2)}")

    def error(self, reqId: TickerId, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print("error",reqId, errorCode, errorString, advancedOrderRejectJson)

def run_loop():
    app.run()

app = TestApp()
app.connect("127.0.0.1", 7496, 1001)

api_thread = threading.Thread(target=run_loop, daemon=True)
api_thread.start()

time.sleep(1)

app.reqPnL(26, "DU74650", "")
app.reqPnL(27, "DU74649", "")

time.sleep(10)
app.disconnect()