from ibapi.client import *
from ibapi.wrapper import *


class TestApp(EClient, EWrapper):

    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        execFilter = ExecutionFilter()
        '''
        The list below represents the available fields and their formatting for the ExecutionFilter object. 

        execFilter.lastNDays = 7
        execFilter.time = "20250410 11:19:00 America/Chicago"
        execFilter.acctCode = "U1234567"
        execFilter.time = "11:19:00 America/Chicago"
        execFilter.exchange = "CBOE"
        execFilter.secType = "OPT"
        execFilter.side = "BUY"
        execFilter.symbol = "SPX"
        execFilter.clientId = 0 
        '''
        
        self.reqExecutions(
            reqId=orderId, 
            execFilter=execFilter
        )


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
app.connect(host="127.0.0.1", port=7497, clientId=0)
app.run()
