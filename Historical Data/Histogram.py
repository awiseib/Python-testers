from ibapi.client import *
from ibapi.common import HistogramData
from ibapi.wrapper import *
port = 7496

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        
        mycontract = Contract()

        mycontract.symbol = "AAPL"
        mycontract.secType = "STK"
        mycontract.exchange = "SMART"
        mycontract.currency = "USD"

        self.reqHistogramData(tickerId=orderId, contract=mycontract, useRTH=True, timePeriod="3 mins")

    def histogramData(self, reqId: int, items: HistogramData):
        print(reqId, items)
        print('\n')
        print("HistogramData. ReqId:", reqId, "HistogramDataList:", "[%s]" % "; ".join(map(str, items)))
        self.cancelHistogramData(reqId)
        
    def error(self, reqId: TickerId, errorTime: int, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(f"Error., Time of Error: {errorTime}, Error Code: {errorCode}, Error Message: {errorString}")
        if advancedOrderRejectJson != "":
            print(f"AdvancedOrderRejectJson: {advancedOrderRejectJson}")

app = TestApp()
app.connect("127.0.0.1", port, 0)
app.run()