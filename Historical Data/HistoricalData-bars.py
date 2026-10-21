from ibapi.client import *
from ibapi.common import TickerId
from ibapi.wrapper import *
from datetime import datetime
from threading import Thread
from time import sleep

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)
    
    def nextValidId(self, orderId):
        mycontract = Contract()
        mycontract.symbol = "AAPL"
        mycontract.secType = "STK"
        mycontract.exchange = "SMART"
        mycontract.currency = "USD"

        self.reqHistoricalData(
            reqId=123,
            contract=mycontract,  
            durationStr= "5 D",
            endDateTime="",
            barSizeSetting = "1 day",
            whatToShow= "TRADES",       # See https://www.interactivebrokers.com/docs/tws-api/doc/md/historical-bars#whattoshow-values for all values. 
            useRTH=1,
            formatDate=1,
            keepUpToDate=False,
            chartOptions=[]
        )
    
    def historicalData(self, reqId, bar):
        print(f"Time: {bar.date}, Open: {bar.open}, High: {bar.high}, Low: {bar.low}, Close: {bar.close}, Volume: {bar.volume}, count: {bar.barCount}")

    def historicalSchedule(self, reqId, startDateTime, endDateTime, timeZone, sessions):
         print(reqId, startDateTime, endDateTime, timeZone, sessions)

    def historicalDataEnd(self, reqId, start, end):
        print(f"Historical Data Ended for {reqId}. Started at {start}, ending at {end}")
        self.disconnect()

    def error(self, reqId: TickerId, errorTime: int, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(f"Error., Time of Error: {errorTime}, Error Code: {errorCode}, Error Message: {errorString}")
        if advancedOrderRejectJson != "":
            print(f"AdvancedOrderRejectJson: {advancedOrderRejectJson}")

app = TestApp()
app.connect(host="127.0.0.1", port=7497, clientId=0)
app.run()