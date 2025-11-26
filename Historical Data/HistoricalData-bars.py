from ibapi.client import *
from ibapi.common import TickerId
from ibapi.wrapper import *
from datetime import datetime

port = 7496

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)
        self.bar_count = 0

    def nextValidId(self, orderId: OrderId):
        mycontract = Contract()
        # mycontract.conId = 132803412=
        # mycontract.exchange = "SMART"
        # mycontract.includeExpired = True
        mycontract.symbol = "AAPL"
        mycontract.secType = "STK"
        mycontract.currency = "USD"
        mycontract.exchange = "SMART"
        # mycontract.primaryExchange = "ISLAND"
        
        self.reqHistoricalData(orderId, mycontract, 
                               endDateTime="", 
                            #    endDateTime="20250924-17:52:08", 
                               durationStr="1 W", 
                               barSizeSetting="1 day", 
                               whatToShow="TRADES", 
                               useRTH=1, 
                               formatDate=1, 
                               keepUpToDate=False, 
                               chartOptions=[]
                               )
    
    def historicalData(self, reqId, bar):
    #     # real_date = bar.date.split(" ")[0]
        # if bar.date == "20251009":
            print(f"Time: {bar.date}, Open: {bar.open}, High: {bar.high}, Low: {bar.low}, Close: {bar.close}, Volume: {bar.volume}")

    def historicalDataEnd(self, reqId, start, end):
        print(f"Historical Data Ended for {reqId}. Started at {start}, ending at {end}")
        self.cancelHistoricalData(reqId)
        self.disconnect()

    def error(self, reqId: TickerId, errorTime: int, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(f"Error., Time of Error: {errorTime}, Error Code: {errorCode}, Error Message: {errorString}")
        if advancedOrderRejectJson != "":
            print(f"AdvancedOrderRejectJson: {advancedOrderRejectJson}")

app = TestApp()
app.connect("127.0.0.1", port, 0)
app.run()