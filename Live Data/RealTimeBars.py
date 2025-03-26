from decimal import Decimal
from ibapi.client import *
from ibapi.common import TickerId
from ibapi.wrapper import *
from ibapi.tag_value import *
from datetime import datetime

port = 7496


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):

        mycontract = Contract()
        mycontract.conId = 265598
        mycontract.exchange = "SMART"

        self.reqRealTimeBars(orderId, mycontract, 5, "TRADES", True, [])

    def realtimeBar(self, reqId: int, time: int, open_: float, high: float, low: float, close: float, volume: Decimal, wap: Decimal, count: int):
        print(f"reqId: {reqId}, Bar Time: {time}, Open: {open_}, High: {high}, Low: {low}, Close: {close}, Volume: {volume}, Weighted Average Price: {wap}, Count: {count}")

    def error(self, reqId: TickerId, errorTime: int, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(f"Error., Time of Error: {errorTime}, Error Code: {errorCode}, Error Message: {errorString}")
        if advancedOrderRejectJson != "":
            print(f"AdvancedOrderRejectJson: {advancedOrderRejectJson}")

app = TestApp()
app.connect("127.0.0.1", port, 0)
app.run()
