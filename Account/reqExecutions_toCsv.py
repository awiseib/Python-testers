from ibapi.client import *
from ibapi.wrapper import *
import csv

port = 7496
DESTINATION = open("C:\\Users\\awise\\Desktop\\executions.csv", "a")
CSVWRITER = csv.writer(DESTINATION)

class TestApp(EClient, EWrapper):


    global execution_count
    execution_count = 0
    global commission_count
    commission_count = 0

    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):

        exec_filter = ExecutionFilter()
        exec_filter.time = "20220621 00:00:00"
        csvHead = ["reqId", "contract", "Exchange", "Price", "Shares"]
        CSVWRITER.writerow(csvHead)

        self.reqExecutions(
            12345,
            exec_filter
        )

    def execDetails(self, reqId: int, contract: Contract, execution: Execution):
        rowDetails = [reqId,contract, execution.exchange, execution.price, execution.shares, execution.cumQty]
        CSVWRITER.writerow(rowDetails)
        global execution_count
        execution_count = execution_count + 1

    def execDetailsEnd(self, reqId: int):
        global execution_count
        global commission_count
        print(execution_count)
        print(commission_count)
        print("execDetailsEnd.", reqId)
        DESTINATION.close()

    def error(self, reqId: TickerId, errorCode: int, errorString: str):
        print(f"error. reqId:{reqId} code:{errorCode} string:{errorString}")


app = TestApp()
app.connect("127.0.0.1", port, 1001)
app.run()
