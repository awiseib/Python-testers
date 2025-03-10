from ibapi.client import *
from ibapi.wrapper import *

port = 7496

class TestApp(EClient, EWrapper):

    def __init__(self):
        EClient.__init__(self, self)
        self.orderId = 0
        self.exec_and_comms = {}

    def nextValidId(self, orderId: OrderId):

        execFilter = ExecutionFilter()
        execFilter.acctCode = ""
        execFilter.time = ""
        execFilter.exchange = ""
        execFilter.secType = ""
        execFilter.side = ""
        execFilter.symbol = ""
        execFilter.clientId = ""

        self.reqExecutions(self.orderId, execFilter)


    def execDetails(self, reqId: int, contract: Contract, execution: Execution):
        self.exec_and_comms[execution.execId] =  {"execDetails": execution}

    def commissionAndFeesReport(self, commissionAndFeesReport: CommissionAndFeesReport):
        self.exec_and_comms[commissionAndFeesReport.execId]["CommReport"] = commissionAndFeesReport

    def execDetailsEnd(self, reqId: int):
        print("execDetailsEnd.", reqId)
        print(
            "\n".join(f"{name}: {value}" for name, value in self.exec_and_comms.items())
        )

app = TestApp()
app.connect("127.0.0.1", port, 0)
app.run()
