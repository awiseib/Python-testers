from decimal import Decimal
from ibapi.client import *
from ibapi.common import TickAttrib, TickerId
from ibapi.wrapper import *
from datetime import datetime
from ibapi.ticktype import TickTypeEnum
port = 7496

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        mycontract = Contract()
        mycontract.conId = 265598
        mycontract.exchange = "SMART"
        # self.reqMarketDataType(4)
        self.reqMktData(
            reqId=self.clientId,
            contract=mycontract,
            genericTickList="",
            snapshot=False,
            regulatorySnapshot=False,
            mktDataOptions=[],
        )
        
    # def tickOptionComputation(self, reqId: TickerId, tickType: TickType, tickAttrib: int, impliedVol: float, delta: float, optPrice: float, pvDividend: float, gamma: float, vega: float, theta: float, undPrice: float):
    #     print(f"tickOptionComputation. reqId: {reqId}, tickType: {TickTypeEnum.toStr(tickType)}, tickAttrib: {tickAttrib}, ImpVol: {impliedVol}, delta: {delta}, optPrice: {optPrice}, pvDividend: {pvDividend}, gamma: {gamma}, vega: {vega}, theta: {theta}, undPrice: {undPrice}")
    
    def tickPrice(self, reqId: TickerId, tickType: TickerId, price: float, attrib: TickAttrib):
        if TickTypeEnum.toStr(tickType) in ["OPEN", "HIGH", "LOW", "CLOSE"]:
            print(f"tickPrice. reqId: {reqId}, tickType: {TickTypeEnum.toStr(tickType)}, price: {price}, attrib: {attrib}")

    # def tickReqParams(self, tickerId: TickerId, minTick: float, bboExchange: str, snapshotPermissions: TickerId):
    #     print(tickerId, minTick, bboExchange, snapshotPermissions)

    # def tickSize(self, reqId: TickerId, tickType: TickType, size: Decimal):
    #     print(f"tickSize. reqId:{reqId}, tickType:{TickTypeEnum.toStr(tickType)}, size:{size}")

    # def tickGeneric(self, reqId: TickerId, tickType: TickType, value: float):
    #     print(f"tickGeneric:  reqId: {reqId}, tickType: {TickTypeEnum.toStr(tickType)}, value: {value}")

    # def tickString(self, reqId: TickerId, tickType: TickType, value: str):
    #     print("tickString: ", reqId, TickTypeEnum.toStr(tickType), value)
        
    # def tickNews(self, tickerId: int, timeStamp: int, providerCode: str, articleId: str, headline: str, extraData: str):
    #     print("tickNews",tickerId, timeStamp, providerCode, articleId, headline, extraData)

    # def tickSnapshotEnd(self, reqId: int):
    #     print(f"tickSnapshotEnd. reqId:{reqId}")
    #     self.disconnect()

    def error(self, reqId: TickerId, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(reqId, errorCode, errorString, advancedOrderRejectJson)

app = TestApp()
app.connect("127.0.0.1", port, 1000)
app.run()