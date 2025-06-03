from ibapi.client import *
from ibapi.common import TickerId
from ibapi.wrapper import *
from datetime import datetime

port = 7497

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        mycontract = Contract()
        mycontract.conId = 3691937
        mycontract.secType = "STK"
        # mycontract.currency = "USD"
        mycontract.exchange = "SMART"
        mycontract.primaryExchange = "NASDAQ"
        self.reqHistoricalData(orderId, mycontract, "", "7 D", "1 hour", "TRADES", 1, 1, True, [])
    
    def historicalData(self, reqId, bar):
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