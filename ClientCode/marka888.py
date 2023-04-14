from decimal import Decimal
from ibapi.client import *
from ibapi.wrapper import *
from datetime import datetime
from ibapi.ticktype import TickTypeEnum
from ibapi.contract import ComboLeg

port = 7496


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
         
        mycontract = Contract()
        # mycontract.conId = 265598 # AAPL STK
        # mycontract.exchange = "SMART"
        
        # mycontract.conId = 495512572 # ES FUT
        # mycontract.exchange = "CME"
        
        mycontract.conId = 615990665 # SPY OPT
        mycontract.exchange = "SMART"

        self.reqMktData(
            reqId=orderId,
            contract=mycontract,
            genericTickList="595",
            snapshot=False,
            regulatorySnapshot=False,
            mktDataOptions=[],
        )

    # def tickOptionComputation(self, reqId: TickerId, tickType: TickType, tickAttrib: int, impliedVol: float, delta: float, optPrice: float, pvDividend: float, gamma: float, vega: float, theta: float, undPrice: float):
    #     print(f"tickOptionComputation. reqId: {reqId}, tickType: {(tickType)}, tickAttrib: {tickAttrib}, ImpVol: {impliedVol}, delta: {delta}, optPrice: {optPrice}, pvDividend: {pvDividend}, gamma: {gamma}, vega: {vega}, theta: {theta}, undPrice: {undPrice}")

    
    def tickPrice(
        self,
        reqId: TickerId,
        tickType: TickType,
        price: float,
        attrib: TickAttrib,
    ):
        print(
            "tickPrice.",
            datetime.now(),
            f"reqId:{reqId}",
            f"tickType:{(tickType)}",
            f"price:{price}",
            f"attrib:{attrib}"
        )


    def tickSize(self, reqId: TickerId, tickType: TickType, size: Decimal):
        print(f"tickSize. reqId:{reqId}, tickType:{(tickType)}, size:{size}")

    def tickGeneric(self, reqId: TickerId, tickType: TickType, value: float):
        print(f"tickGeneric:  reqId: {reqId}, tickType: {(tickType)}, value: {value}")

    def tickString(self, reqId: TickerId, tickType: TickType, value: str):
        print("tickString: ", reqId, (tickType), value)
        
    def tickNews(self, tickerId: int, timeStamp: int, providerCode: str, articleId: str, headline: str, extraData: str):
        print("tickNews",tickerId, timeStamp, providerCode, articleId, headline, extraData)

    # def tickSnapshotEnd(self, reqId: int):
    #     print(f"tickSnapshotEnd. reqId:{reqId}")
    #     self.disconnect()

    # def error(self, reqId: TickerId, errorCode: int, errorString: str, advancedOrderRejectJson=""):
    #     return super().error(reqId, errorCode, errorString, advancedOrderRejectJson)

app = TestApp()
app.connect("127.0.0.1", port, 100)
app.run()