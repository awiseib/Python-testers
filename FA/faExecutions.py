from ibapi.client import *
from ibapi.wrapper import *

port = 7496

class TestApp(EClient, EWrapper):

    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):

        exec_filter = ExecutionFilter()
        exec_filter.acctCode = "DU74649"

        self.reqExecutions(
            12345,
            exec_filter
        )

    def execDetails(self, reqId: int, contract: Contract, execution: Execution):
        print(reqId, contract, execution)

    def execDetailsEnd(self, reqId: int):
        print("execDetailsEnd.", reqId)
        self.disconnect()


app = TestApp()
app.connect("127.0.0.1", port, 1007)
app.run()
