from ibapi.client import *
from ibapi.wrapper import *
from ibapi.contract import ComboLeg

port = 7496


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        
        contract = Contract()
        contract.exchange = "OVERNIGHT"
        contract.symbol = "AAPL"
        contract.secType = "STK"
        contract.currency = "USD"
        # contract.lastTradeDateOrContractMonth = "202406"
        # contract.includeExpired = True

        self.reqHistoricalData(
            reqId=14,
            contract=contract,
            # endDateTime="20240327 14:00:00 UTC",
            endDateTime="",
            durationStr="6 D",
            barSizeSetting="1 day",
            whatToShow="schedule",
            useRTH=1,
            formatDate=1,
            keepUpToDate=False,
            chartOptions=[]
        )

    def historicalData(self, reqId: int, bar: BarData):
        print(reqId, bar)
        
    def historicalSchedule(self, reqId: int, startDateTime: str, endDateTime: str, timeZone: str, sessions: ListOfHistoricalSessions):
         print(reqId, startDateTime, endDateTime, timeZone, sessions)

    def historicalDataEnd(self, reqId: int, start: str, end: str):
        print(reqId, start, end)
        self.disconnect()

app = TestApp()
app.connect("127.0.0.1", port, 1001)
app.run()
