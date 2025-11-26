from decimal import Decimal
from ibapi.client import *
from ibapi.common import BarData, TickAttrib, TickerId
from ibapi.contract import Contract, ContractDetails
from ibapi.order import Order
from ibapi.order_state import OrderState
from ibapi.wrapper import *
from ibapi.account_summary_tags import *

import threading, time

port = 7496

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)
        self.oid = 0

    def nextValidId(self, orderId: OrderId):
        self.oid = orderId

    def nextOid(self):
        self.oid += 1
        return self.oid
    
    def accountSummaryEnd(self, reqId: TickerId):
        print("--> Account Summary End")

    def positionEnd(self):
        print("--> Position End")

    def pnl(self, reqId: TickerId, dailyPnL: float, unrealizedPnL: float, realizedPnL: float):
        print("--> PNL End")

    def completedOrdersEnd(self):
        print("--> Completed Orders")
    
    def execDetailsEnd(self, reqId: TickerId):
        print("Executions", reqId)

    def contractDetailsEnd(self, reqId: TickerId):
        print(f"--> Contract Details {reqId}")

    def historicalDataEnd(self, reqId: TickerId, start: str, end: str):
        print("--> historical Data")
    
    def tickPrice(self, reqId: TickerId, tickType: TickerId, price: float, attrib: TickAttrib):
        print("--> Tick Price")
        self.cancelMktData(reqId)
    
    def currentTime(self, time: TickerId):
        print("--> Current Time")
    
    def currentTimeInMillis(self, timeInMillis: TickerId):
        print("--> Current Time Millis")

    def historicalNews(self, requestId: TickerId, time: str, providerCode: str, articleId: str, headline: str):
        print("--> Historical News")
    
    def openOrder(self, orderId: TickerId, contract: Contract, order: Order, orderState: OrderState):
        print("--> Open Order")

    def scannerDataEnd(self, reqId: TickerId):
        print("--> Scanner Data")
        self.cancelScannerSubscription(reqId)

    def wshMetaData(self, reqId: TickerId, dataJson: str):
        print("--> WSH Meta Data")

    def wshEventData(self, reqId: TickerId, dataJson: str):
        print("--> WSH EVENT DATA")
    
    def error(self, reqId: TickerId, errorTime: int, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(f"Error., Time of Error: {errorTime}, Error Code: {errorCode}, Error Message: {errorString}")
        if advancedOrderRejectJson != "":
            print(f"AdvancedOrderRejectJson: {advancedOrderRejectJson}")


app = TestApp()
app.connect("127.0.0.1", port, 0)
time.sleep(3)
threading.Thread(target=app.run).start()
time.sleep(1)

con = Contract()
con.conId = 265598
con.exchange = "SMART"

o = Order()
o.action = "BUY"
o.orderType = "MKT"
o.totalQuantity = 10

sub = ScannerSubscription()
sub.instrument = "STK"
sub.locationCode = "STK.US.MAJOR"
sub.scanCode = "MOST_ACTIVE"

eventData = WshEventData()
eventData.filter = '{"country": "All","watchlist":["265598"], "wshe_eps":"true"}'


# Account
print("<-- reqPositions")
app.reqPositions()
print("<-- reqCompletedOrders")
app.reqCompletedOrders(False)

print("<-- reqOpenOrders")
app.reqOpenOrders()

oid = app.nextOid()
app.reqAccountSummary(oid, "All", AccountSummaryTags.AllTags)
print(f"<-- Order ID {oid} reqAccountSummary!")

oid = app.nextOid()
app.reqPnL(oid, "DU5240685", "")
print(f"<-- Order ID {oid} reqPnL!")

oid = app.nextOid()
app.reqExecutions(oid, ExecutionFilter())
print(f"<-- Order ID {oid} reqExecutions!")
#Contracts
oid = app.nextOid()
app.reqContractDetails(oid, con)
print(f"<-- Order ID {oid} reqContractDetails!")
# Historical Data
oid = app.nextOid()
app.reqHistoricalData(oid, con, "", "1 W", "1 day", "TRADES", 1, 1, False, [])
print(f"<-- Order ID {oid} reqHistoricalData!")
# Live Data
oid = app.nextOid()
app.reqMktData(oid, con, "", False, False, [])
print(f"<-- Order ID {oid} reqMktData!")
# News
oid = app.nextOid()
app.reqHistoricalNews(oid, 265598, "DJNL", "20250101 00:00:01", "", 5, [] )
print(f"<-- Order ID {oid} reqHistoricalNews!")
# Orders
oid = app.nextOid()
app.placeOrder(oid, con, o)
print(f"<-- Order ID {oid} placeOrder!")
# Scanner
oid = app.nextOid()
app.reqScannerSubscription(oid, sub, [], [])
print(f"<-- Order ID {oid} reqScannerSubscription!")
# Wall Street Horizons
oid = app.nextOid()
app.reqWshMetaData(oid)
print(f"<-- Order ID {oid} reqWshMetaData!")
oid = app.nextOid()
app.reqWshEventData(oid, eventData)
print(f"<-- Order ID {oid} reqWshEventData!")