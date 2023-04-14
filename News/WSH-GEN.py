from http import client
from ibapi.client import *
from ibapi.wrapper import *

port = 7496


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):

        mycontract = Contract()
        mycontract.symbol="AAPL"
        mycontract.secType="STK"
        mycontract.exchange="SMART"
        mycontract.currency="USD"

        self.reqWshMetaData(1100)

    def wshMetaData(self, reqId: TickerId, data: str):
        print(
            "fundamentalData.",
            f"reqId:{reqId}",
            f"data:{data}",
        )

app = TestApp()
app.connect("127.0.0.1", port, 1001)
app.run()
