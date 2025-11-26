from ibapi.client import *
from ibapi.wrapper import *
from datetime import datetime

port = 7497


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        
        mycontract = Contract()
        mycontract.conId = 265598
        # mycontract.symbol = "AAPL"
        # mycontract.secType = "STK"
        # mycontract.currency = "USD"
        mycontract.exchange = "SMART"
        
        
        self.reqHistoricalData(
            reqId=123,
            contract=mycontract,
            endDateTime="",
            durationStr= "4800 S",
            barSizeSetting = "4 mins",
            whatToShow= "TRADES",
            useRTH=0,
            formatDate=1,
            keepUpToDate=False,
            chartOptions=[],
        )
        

    def historicalData(self, reqId: int, bar: BarData):
        print("DATA", reqId, bar)

    def historicalDataUpdate(self, reqId: int, bar: BarData):
        print(f"UPDATE. Current Time: {datetime.now().time()}; Bar Time: {bar.date}, O: {bar.open}; H: {bar.high}; L: {bar.low}; C: {bar.close}")
        
    # def historicalDataEnd(self, reqId: int, start: str, end: str):
    #     print("historicalDataEnd")

    def error(self, reqId: TickerId, errorTime: int, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(f"Error., Time of Error: {errorTime}, Error Code: {errorCode}, Error Message: {errorString}")
        if advancedOrderRejectJson != "":
            print(f"AdvancedOrderRejectJson: {advancedOrderRejectJson}")

app = TestApp()
app.connect("127.0.0.1", port, 0)
app.run()
 