from ibapi.client import *
from ibapi.wrapper import *
from ibapi.account_summary_tags import *
from functools import partial
# from printcalls import *


port = 7496

# @all(echo)
class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        
        self.reqAccountSummary(
            reqId=12345,
            groupName="All",
            tags=AccountSummaryTags.AllTags
        )

    def accountSummary(self, reqId: int, account: str, tag: str, value: str, currency: str):
        print(reqId, account, tag, value, currency)

    def accountSummaryEnd(self, reqId: int):
        print("End of Account Summary")
        self.disconnect()

    def error(
        self,
        reqId: TickerId,
        errorCode: int,
        errorString: str,
        advancedOrderRejectJson="",
    ):
        print(
            "error.",
            f"reqId:{reqId}",
            f"errorCode:{errorCode}",
            f"errorString:{errorString}",
            f"advancedOrderRejectJson:{advancedOrderRejectJson}",
        )

app = TestApp()
app.connect("127.0.0.1", port, 1001)
app.run()
