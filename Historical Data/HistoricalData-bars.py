from socket import timeout
from symtable import Symbol
from ibapi.client import *
from ibapi.wrapper import *
import datetime
import time
from ibapi.tag_value import TagValue
from ibapi.contract import ComboLeg
import threading
datetime.datetime.now()
port = 7496


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        
        mycontract = Contract()
        # mycontract.conId = 575209133
        mycontract.localSymbol = "ESU1"

        # mycontract.symbol = "DAX"
        mycontract.secType = "FUT"
        mycontract.exchange = "CME"
        mycontract.currency = "USD"
        mycontract.includeExpired = True

        # mycontract.primaryExchange = "ARCA"
        # mycontract.lastTradeDateOrContractMonth = 20230321
        # mycontract.right = "C"
        # mycontract.strike = 3850

        self.reqHistoricalData(
            reqId=orderId,
            contract=mycontract,
            endDateTime="20210913 14:35:00 US/Central",
            # endDateTime="",
            durationStr= "1 D",
            barSizeSetting = "1 hour",
            whatToShow= "TRADES", 
			useRTH=0, 
			formatDate=1, 
			keepUpToDate=0,
			chartOptions=[]
        )

    def historicalData(self, reqId: int, bar: BarData):
        # if bar.open == bar.close:
            print(reqId, bar)


    def historicalDataEnd(self, reqId: int, start: str, end: str):
        print(reqId, start, end)
        self.disconnect()

    # def error(self, reqId: TickerId, errorCode: int, errorString: str, advancedOrderRejectJson=""):
    #     print(reqId, errorCode, errorString, advancedOrderRejectJson)



app = TestApp()
app.connect("127.0.0.1", port, 1001)
app.run()
