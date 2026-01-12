from decimal import Decimal
from ibapi.client import *
from ibapi.common import TickAttrib, TickerId
from ibapi.wrapper import *
from ibapi.ticktype import TickTypeEnum
import time, threading
from ibapi.contract import ComboLeg

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def tickPrice(self, reqId: TickerId, tickType: TickerId, price: float, attrib: TickAttrib):
        print(f"tickPrice. reqId: {reqId}, tickType: {TickTypeEnum.toStr(tickType)}, price: {price}, attrib: {attrib}")

    def tickSize(self, reqId: TickerId, tickType: TickType, size: Decimal):
        print(f"tickSize. reqId:{reqId}, tickType:{TickTypeEnum.toStr(tickType)}, size:{size}")

    def tickReqParams(self, tickerId: TickerId, minTick: float, bboExchange: str, snapshotPermissions: TickerId):
        print(tickerId, minTick, bboExchange, snapshotPermissions)

    def rerouteMktDataReq(self, reqId: TickerId, conId: TickerId, exchange: str):
        print("Reroute CFD data:", conId, exchange)

    def tickOptionComputation(self, reqId: TickerId, tickType: TickType, tickAttrib: int, impliedVol: float, delta: float, optPrice: float, pvDividend: float, gamma: float, vega: float, theta: float, undPrice: float):
        print(f"tickOptionComputation. reqId: {reqId}, tickType: {TickTypeEnum.toStr(tickType)}, tickAttrib: {tickAttrib}, ImpVol: {impliedVol}, delta: {delta}, optPrice: {optPrice}, pvDividend: {pvDividend}, gamma: {gamma}, vega: {vega}, theta: {theta}, undPrice: {undPrice}")
    
    def tickGeneric(self, reqId: TickerId, tickType: TickType, value: float):
        print(f"tickGeneric:  reqId: {reqId}, tickType: {TickTypeEnum.toStr(tickType)}, value: {value}")

    def tickString(self, reqId: TickerId, tickType: TickType, value: str):
        print("tickString: ", reqId, TickTypeEnum.toStr(tickType), value)
        
    def tickNews(self, tickerId: int, timeStamp: int, providerCode: str, articleId: str, headline: str, extraData: str):
        print("tickNews",tickerId, timeStamp, providerCode, articleId, headline, extraData)

    def rerouteMktDepthReq(self, reqId, conId, exchange):
        print("rerouteMktDepthReq", reqId, conId, exchange)

    def tickSnapshotEnd(self, reqId: int):
        print(f"tickSnapshotEnd. reqId:{reqId}")
        self.disconnect()

    def error(self, reqId: TickerId, errorTime: int, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(f"Error., Time of Error: {errorTime}, Error Code: {errorCode}, Error Message: {errorString}")
        if advancedOrderRejectJson != "":
            print(f"AdvancedOrderRejectJson: {advancedOrderRejectJson}")
        

app = TestApp()
app.connect("127.0.0.1", 7496, 10)
time.sleep(1)
threading.Thread(target=app.run).start()
time.sleep(1)

app.reqMarketDataType(3)

contract = Contract()
contract.conId = 265598
# contract.symbol = "SPX"
# contract.secType = "OPT"
# contract.currency = "USD"
contract.exchange = "SMART"
# contract.strike = 6850
# contract.lastTradeDateOrContractMonth = "20260115"
# contract.right = "P"
# contract.tradingClass = "SPX"

app.reqMktData(
    reqId=101,
    contract=contract,
    genericTickList="236",
    snapshot=0,
    regulatorySnapshot=0,
    mktDataOptions= []
)
