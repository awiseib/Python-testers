from ibapi.client import *
from ibapi.wrapper import *
from ibapi.account_summary_tags import *


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        
        self.reqAccountSummary(
            reqId       =orderId,
            groupName   ="All",
            tags        =AccountSummaryTags.AllTags # The full list of AccountSummaryTags are visible from ibapi/account_summary_tags
        )

    def accountSummary(self, reqId: int, account: str, tag: str, value: str, currency: str):
        print(reqId, account, tag, value, currency)

    def accountSummaryEnd(self, reqId: int):
        print("End of Account Summary")
        self.disconnect()

    def error(self, reqId: TickerId, errorTime: int, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(f"Error., Time of Error: {errorTime}, Error Code: {errorCode}, Error Message: {errorString}")
        if advancedOrderRejectJson != "":
            print(f"AdvancedOrderRejectJson: {advancedOrderRejectJson}")

app = TestApp()
app.connect(host="127.0.0.1", port=7497, clientId=0)
app.run()
