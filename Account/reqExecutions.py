from ibapi.client import *
from ibapi.wrapper import *

port = 7496

class TestApp(EClient, EWrapper):

    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        execFilter = ExecutionFilter()
        # execFilter.acctCode = ""
        # execFilter.time = ""
        # execFilter.exchange = ""
        # execFilter.secType = ""
        # execFilter.side = ""
        # execFilter.symbol = ""
        # execFilter.clientId = ""

        self.reqExecutions(self.orderId, execFilter)


    def execDetails(self, reqId: int, contract: Contract, execution: Execution):
        print("execDetails: ", contract, execution)

    def commissionAndFeesReport(self, commissionAndFeesReport: CommissionAndFeesReport):
        print("commission: ", commissionAndFeesReport)

    def execDetailsEnd(self, reqId: int):
        print("execDetailsEnd.", reqId)

    def error(self, reqId: TickerId, errorTime: int, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(f"Error., Time of Error: {errorTime}, Error Code: {errorCode}, Error Message: {errorString}")
        if advancedOrderRejectJson != "":
            print(f"AdvancedOrderRejectJson: {advancedOrderRejectJson}")

app = TestApp()
app.connect("127.0.0.1", port, 0)
app.run()
