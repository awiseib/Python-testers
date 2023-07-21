from ibapi.client import *
from ibapi.wrapper import *
import datetime

port = 7496


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):

        mycontract = Contract()
        mycontract.conId = 605247013
        # mycontract.localSymbol = "ESU1"

        # mycontract.symbol = "MTEK"
        # mycontract.secType = "STK"
        mycontract.exchange = "CBOT"
        # mycontract.currency = "USD"

        self.reqHistoricalTicks(
            reqId=123,
            contract=mycontract,
            startDateTime="",
            endDateTime="20230629 08:45:00 US/Central",
            numberOfTicks=1000,
            whatToShow="Bid_Ask",
            useRth=1,
            ignoreSize=True,
            miscOptions=[],
        )

    def historicalTicksLast(
        self, 
        reqId: int, 
        ticks: ListOfHistoricalTickLast, 
        done: bool,
    ):
        for tick in ticks:
            print(
                "historicalTicksLast.", 
                f"reqId:{reqId}", 
                datetime.datetime.fromtimestamp(tick.time),
                f"ticks:{tick.price}"
            )

    def historicalTicksBidAsk(
        self, 
        reqId: int, 
        ticks: ListOfHistoricalTickBidAsk, 
        done: bool,
    ):
        for tick in ticks:
            print(
                "historicalTicksBidAsk.", 
                # f"reqId:{reqId}", 
                # datetime.datetime.fromtimestamp(tick.time),
                f"ticks:{tick}"
            )

    def historicalTicks(
        self, 
        reqId: int, 
        ticks: ListOfHistoricalTick, 
        done: bool,
    ):
        for tick in ticks:
            print(
                "historicalTicksLast.", 
                f"reqId:{reqId}", 
                datetime.datetime.fromtimestamp(tick.time),
                f"ticks:{tick.price}"
            )


app = TestApp()
app.connect("127.0.0.1", port, 1001)
app.run()
