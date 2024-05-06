from ibapi.client import *
from ibapi.wrapper import *
from datetime import datetime
port = 7496


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):

        mycontract = Contract()
        mycontract.conId = 265598
        # mycontract.symbol = "IBCID559139897"
        # mycontract.secType = "BOND"
        # mycontract.currency = "USD"
        mycontract.exchange = "SMART"



        self.reqTickByTickData(
            reqId=123,
            contract=mycontract,
            tickType="MidPoint",
            numberOfTicks=50,
            ignoreSize=0
        )

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
        

    def tickSnapshotEnd(self, reqId: int):
        print(f"tickSnapshotEnd. reqId:{reqId}")


app = TestApp()
app.connect("127.0.0.1", port, 1001)
app.run()
