from ibapi.client import *
from ibapi.wrapper import *
from ibapi.contract import ComboLeg

port = 7496


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        
        mycontract = Contract()
        mycontract.conId = 457068913
        # mycontract.symbol = "AAPL"
        # mycontract.secType = "STK"
        # mycontract.currency = "USD"
        mycontract.exchange = "SMART"
        
        
        self.reqHistoricalData(
            reqId=orderId,
            contract=mycontract,
            # endDateTime="20230724-15:52:00",
            # endDateTime="20230728 13:56:00 UTC",
            endDateTime="",
            durationStr= "1 D",
            barSizeSetting = "1 day",
            whatToShow= "bid_ask", 
            useRTH=0, 
            formatDate=1, 
            keepUpToDate=0,
            chartOptions=[]
        )

    def historicalData(self, reqId: int, bar: BarData):
        # if bar.open == bar.close:
            print(reqId, bar)
            bar.date
            # print(bar.timeZoneId)
        
    # def historicalSchedule(self, reqId: int, startDateTime: str, endDateTime: str, timeZone: str, sessions: ListOfHistoricalSessions):
    #      print(reqId, startDateTime, endDateTime, timeZone, sessions)


    def historicalDataEnd(self, reqId: int, start: str, end: str):
        print(reqId, start, end)
        self.disconnect()

    # def error(self, reqId: TickerId, errorCode: int, errorString: str, advancedOrderRejectJson=""):
    #     print(reqId, errorCode, errorString, advancedOrderRejectJson)



app = TestApp()
app.connect("127.0.0.1", port, 1001)
app.run()
