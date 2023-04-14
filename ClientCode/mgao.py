from ibapi.client import *
from ibapi.wrapper import *
import threading
import datetime

port = 7496


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def historicalTicksLast(self, reqId: int, ticks: ListOfHistoricalTickLast, done: bool):
        print(reqId, len(ticks))


app = TestApp()
app.connect("127.0.0.1", port, 1001)

threading.Thread(target=app.run).start()


mycontract = Contract()
mycontract.symbol = "AAPL"
mycontract.secType = "STK"
mycontract.currency = "USD"
mycontract.exchange = "SMART"

hrs = 15
mins = 59
secs = 00
reqIds=100

for i in range(0,5):
    app.reqHistoricalTicks(
        reqId=reqIds,
        contract=mycontract,
        startDateTime="",
        endDateTime=f"20221103 {hrs}:{mins}:{secs} US/Eastern",
        numberOfTicks=1000,
        whatToShow="Trades",
        useRth=1,
        ignoreSize=True,
        miscOptions=[],
    )
    reqIds+=1
    mins -= 5