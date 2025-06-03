from ibapi.client import *
from ibapi.wrapper import *
import datetime

port = 7496


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):

        mycontract = Contract()
        mycontract.conId = 772144625
        mycontract.exchange = "SMART"

        self.reqHistoricalTicks(
            reqId=orderId,
            contract=mycontract,
            startDateTime="",
            endDateTime="20250423 10:34:00 US/Eastern",
            numberOfTicks=100,
            whatToShow="AllLast",
            useRth=1,
            ignoreSize=False,
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
        # self.disconnect()

    def historicalTicksBidAsk(
        self, 
        reqId: int, 
        ticks: ListOfHistoricalTickBidAsk, 
        done: bool,
    ):
        # print(type(ticks[0]))
        for tick in ticks:
            print(
                "historicalTicksBidAsk.", 
                f"ticks:{tick}"
            )
        self.disconnect()

    def historicalTicks(
        self, 
        reqId: int, 
        ticks: ListOfHistoricalTick, 
        done: bool,
    ):
        for tick in ticks:
            print(
                "historicalTicks.", 
                f"reqId:{reqId}", 
                datetime.datetime.fromtimestamp(tick.time,datetime.timezone.tzname("US/Central")),
                f"ticks:{tick.price}"
            )

    def error(self, reqId: TickerId, errorTime: int, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(f"Error., Error Code: {errorCode}, Error Message: {errorString}")
        if advancedOrderRejectJson != "":
            print(f"AdvancedOrderRejectJson: {advancedOrderRejectJson}")


app = TestApp()
app.connect("127.0.0.1", port, 1)
app.run()
