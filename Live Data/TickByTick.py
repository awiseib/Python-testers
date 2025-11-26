from ibapi.client import *
from ibapi.wrapper import *
from datetime import datetime
from threading import Thread
from time import sleep
port = 7496


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    # whatToShow=BidAsk
    def tickByTickBidAsk(self, reqId: int, time: int, bidPrice: float, askPrice: float, bidSize: int, askSize: int, tickAttribBidAsk: TickAttribBidAsk):
        print(f"reqId: {reqId}, time: {datetime.fromtimestamp(time) }, bidPrice: {bidPrice}, askPrice: {askPrice}, bidSize: {bidSize}, askSize: {askSize}, tickAttribBidAsk: {tickAttribBidAsk}")

    # whatToShow=MidPoint
    def tickByTickMidPoint(self, reqId: int, time: int, midPoint: float):
        print(f"reqId: {reqId}, {datetime.fromtimestamp(time)}, {midPoint}")

    # # whatToShow=AllLast
    def tickByTickAllLast(self, reqId: int, tickType: int, time: int, price: float, size: int, tickAttribLast: TickAttribLast, exchange: str, specialConditions: str):
        # Tick type does not correspond to tickType.py
        if tickType == 1:
            print(f"Last. reqId: {reqId}, time: {datetime.fromtimestamp(time)}, price: {price}, size: {size}, tickAttribLast: {tickAttribLast}, exchange: {exchange}, specialConditions: {specialConditions}")
        else:
            print(f"AllLast. reqId: {reqId}, time: {datetime.fromtimestamp(time)}, price: {price}, size: {size}, tickAttribLast: {tickAttribLast}, exchange: {exchange}, specialConditions: {specialConditions}")

    def error(self, reqId: TickerId, errorTime: int, errorCode: int, errorString="", advancedOrderRejectJson=""):
        print(f"Error., Time of Error: {errorTime}, Error Code: {errorCode}, Error Message: {errorString}")
        if advancedOrderRejectJson != "":
            print(f"AdvancedOrderRejectJson: {advancedOrderRejectJson}")
        

app = TestApp()
app.connect("127.0.0.1", port, 0)
sleep(1)
Thread(target=app.run).start()
sleep(1)
app.reqMarketDataType(1)
c1 = Contract()
c1.conId = 265598
c1.exchange = "SMART"
app.reqTickByTickData(1, c1, "AllLast", 50, 0)