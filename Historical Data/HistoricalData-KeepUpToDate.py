from ibapi.client import *
from ibapi.wrapper import *
from datetime import datetime



class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        mycontract = Contract()
        mycontract.symbol = "AAPL"
        mycontract.secType = "STK"
        mycontract.exchange = "SMART"
        mycontract.currency = "USD"        
        
        self.reqHistoricalData(
            reqId=123,
            contract=mycontract,
            endDateTime="",
            durationStr= "4800 S",
            barSizeSetting = "4 mins",
            whatToShow= "TRADES",       # See https://www.interactivebrokers.com/docs/tws-api/doc/md/historical-bars#whattoshow-values for all values. 
            useRTH=0,
            formatDate=1,
            keepUpToDate=True,
            chartOptions=[],
        )
        

    def historicalData(self, reqId: int, bar: BarData):
        print("DATA", reqId, bar)

    def historicalDataUpdate(self, reqId: int, bar: BarData):
        print(f"UPDATE. Current Time: {datetime.now().time()}; Bar Time: {bar.date}, O: {bar.open}; H: {bar.high}; L: {bar.low}; C: {bar.close}")

    def error(self, reqId: TickerId, errorTime: int, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(f"Error., Time of Error: {errorTime}, Error Code: {errorCode}, Error Message: {errorString}")
        if advancedOrderRejectJson != "":
            print(f"AdvancedOrderRejectJson: {advancedOrderRejectJson}")

app = TestApp()
app.connect(host="127.0.0.1", port=7497, clientId=0)
app.run()
 