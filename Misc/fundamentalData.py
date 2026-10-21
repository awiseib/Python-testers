from ibapi.client import *
from ibapi.wrapper import *

port = 7496

requestCodes = {}
for i in range(0, 23):
    requestCodes[i] = {}

class TestApp(EClient, EWrapper):
  def __init__(self):
    EClient.__init__(self, self)

  def nextValidId(self, orderId: int):
    
    contract = Contract()
    # contract.conId = 265598 # AAPL ConId
    contract.symbol = "DJ-TOP"
    contract.currency = "USD"
    contract.secType = "NEWS"
    contract.exchange = "DJNL"

    '''
    reportType:str - One of the following XML reports:
      - ReportSnapshot (company overview)
      - ReportsFinSummary (financial summary)
      - ReportRatios (financial ratios)
      - ReportsFinStatements (financial statements)
      - RESC (analyst estimates)
'''
    self.reqFundamentalData(orderId, contract, "TopNews", [])

  def fundamentalData(self, reqId, data):
    print(data)


app = TestApp()
app.connect("127.0.0.1", port, 1002)
app.run()