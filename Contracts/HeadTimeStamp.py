from socket import timeout
from symtable import Symbol
from ibapi.client import *
from ibapi.wrapper import *
import datetime
from ibapi.tag_value import TagValue

datetime.datetime.now()
port = 7496


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        
        mycontract = Contract()
        mycontract.symbol = "INDU"
        mycontract.secType = "IND"
        mycontract.exchange = "CME"
        mycontract.currency = "USD"

        self.reqHeadTimeStamp(orderId, mycontract, "Trades", 1, 1)

    def headTimestamp(self, reqId: int, headTimestamp: str):
        print(f"headTimeStamp. reqId: {reqId}, headTimestamp: {headTimestamp}")


app = TestApp()
app.connect("127.0.0.1", port, 1001)
app.run()
