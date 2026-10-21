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

        self.reqRealTimeBars(
            reqId=orderId, 
            contract=mycontract, 
            barSize=60, 
            whatToShow="TRADES", 
            useRTH=True, 
            realTimeBarsOptions=[]
        )

    def realtimeBar(self, reqId: int, time: int, open_: float, high: float, low: float, close: float, volume: Decimal, wap: Decimal, count: int):
        print(f"reqId: {reqId}, Bar Time: {datetime.fromtimestamp(time)}, Open: {open_}, High: {high}, Low: {low}, Close: {close}, Volume: {volume}, Weighted Average Price: {wap}, Count: {count}")
        self.cancelRealTimeBars(reqId)
        self.disconnect()

    def error(self, reqId: TickerId, errorTime: int, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(f"Error., Time of Error: {errorTime}, Error Code: {errorCode}, Error Message: {errorString}")
        if advancedOrderRejectJson != "":
            print(f"AdvancedOrderRejectJson: {advancedOrderRejectJson}")

app = TestApp()
app.connect(host="127.0.0.1", port=7497, clientId=0)
app.run()
