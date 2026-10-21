from decimal import Decimal
from ibapi.client import *
from ibapi.common import TickAttrib, TickerId, MarketDataTypeEnum
from ibapi.wrapper import *
from ibapi.ticktype import TickTypeEnum
import time, threading
from ibapi.contract import ComboLeg

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId):
        self.reqMarketDataType(4)

        mycontract = Contract()
        mycontract.symbol = "AAPL"
        mycontract.secType = "STK"
        mycontract.exchange = "SMART"
        mycontract.currency = "USD"

        self.reqMktData(
            reqId=orderId,
            contract=mycontract,
            genericTickList="",     # See https://www.interactivebrokers.com/docs/tws-api/doc/md/streaming-data#available-tick-types for available values.
            snapshot=0,
            regulatorySnapshot=0,
            mktDataOptions= []
        )

    def tickPrice(self, reqId: TickerId, tickType: TickerId, price: float, attrib: TickAttrib):
        print(f"tickPrice. reqId: {reqId}, tickType: {TickTypeEnum.toStr(tickType)}, price: {price}, attrib: {attrib}")
    
    def tickSize(self, reqId: TickerId, tickType: TickType, size: Decimal):
        print(f"tickSize. reqId:{reqId}, tickType:{TickTypeEnum.toStr(tickType)}, size:{size}")

    def tickReqParams(self, tickerId: TickerId, minTick: float, bboExchange: str, snapshotPermissions: TickerId):
        print(f"tickReqParams, tickerId: {tickerId}, minTick: {minTick}, bboExchange: {bboExchange}, snapshotPermissions: {snapshotPermissions}")

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

    def rerouteMktDataReq(self, reqId: TickerId, conId: TickerId, exchange: str):
        print("Reroute CFD data:", conId, exchange)
    
    def marketDataType(self, reqId, marketDataType):
        print(f"Market Data Type: { MarketDataTypeEnum.toStr(marketDataType)}")

    def tickSnapshotEnd(self, reqId: int):
        print(f"tickSnapshotEnd. reqId:{reqId}")
        self.disconnect()

    def error(self, reqId: TickerId, errorTime: int, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(f"Error., Time of Error: {errorTime}, Error Code: {errorCode}, Error Message: {errorString}")
        if advancedOrderRejectJson != "":
            print(f"AdvancedOrderRejectJson: {advancedOrderRejectJson}")
        

app = TestApp()
app.connect(host="127.0.0.1", port=7497, clientId=0)
app.run()