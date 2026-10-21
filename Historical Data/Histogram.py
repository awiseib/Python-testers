from ibapi.client import *
from ibapi.common import HistogramData
from ibapi.wrapper import *

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        
        mycontract = Contract()
        mycontract.symbol = "AAPL"
        mycontract.secType = "STK"
        mycontract.exchange = "SMART"
        mycontract.currency = "USD"

        self.reqHistogramData(
            tickerId=orderId, 
            contract=mycontract, 
            useRTH=True, 
            timePeriod="3 mins"
        )

    def histogramData(self, reqId: int, items: HistogramData):
        print("HistogramData. ReqId:", reqId, "HistogramDataList:", "\n".join(f"{i.price}: {i.size}" for i in items))
        self.cancelHistogramData(reqId)
        self.disconnect()
        
    def error(self, reqId: TickerId, errorTime: int, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(f"Error., Time of Error: {errorTime}, Error Code: {errorCode}, Error Message: {errorString}")
        if advancedOrderRejectJson != "":
            print(f"AdvancedOrderRejectJson: {advancedOrderRejectJson}")

app = TestApp()
app.connect(host="127.0.0.1", port=7497, clientId=0)
app.run()