from ibapi.client import *
from ibapi.wrapper import *
port = 7496

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        
        mycontract = Contract()
        mycontract.conId = 495512552
        mycontract.exchange = "CME"
        # mycontract.symbol = "ES"
        # mycontract.secType = "CONTFUT"
        # mycontract.exchange = "CME"
        # mycontract.currency = "USD"

        self.reqHeadTimeStamp(1, mycontract, "TRADES", 1, 1)

    def headTimestamp(self, reqId: int, headTimestamp):
        print(f"headTimeStamp. reqId: {reqId}, headTimestamp: {headTimestamp}")
        self.cancelHeadTimeStamp(reqId)
        self.disconnect()
        
    def error(self, reqId: TickerId, errorTime: int, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(f"Error., Time of Error: {errorTime}, Error Code: {errorCode}, Error Message: {errorString}")
        if advancedOrderRejectJson != "":
            print(f"AdvancedOrderRejectJson: {advancedOrderRejectJson}")

app = TestApp()
app.connect("127.0.0.1", port, 0)
app.run()