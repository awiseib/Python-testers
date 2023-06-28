from ibapi.client import *
from ibapi.wrapper import *
import datetime

datetime.datetime.now()
port = 7496


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        
        mycontract = Contract()
        mycontract.symbol = "TMUS"
        mycontract.secType = "STK"
        mycontract.exchange = "SMART"
        mycontract.currency = "USD"

        self.reqHeadTimeStamp(orderId, mycontract, "Trades", 1, 1)

    def headTimestamp(self, reqId: int, headTimestamp: str):
        print(f"headTimeStamp. reqId: {reqId}, headTimestamp: {headTimestamp}")


app = TestApp()
app.connect("127.0.0.1", port, 1001)
app.run()
