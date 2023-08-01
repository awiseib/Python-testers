from decimal import Decimal
from ibapi.client import *
from ibapi.wrapper import *
from datetime import datetime
from ibapi.ticktype import TickTypeEnum
from ibapi.contract import ComboLeg
import time

port = 7496
# port = 4002


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
         
        mycontract = Contract()
        mycontract = Contract()
        mycontract.symbol = "SPX"
        mycontract.secType = "BAG"
        mycontract.currency = "USD"
        mycontract.exchange = "SMART"

        leg1 = ComboLeg()
        leg1.conId = 636309066 # SPX 4575 P
        leg1.ratio = 1
        leg1.action = "SELL"
        leg1.exchange = "SMART"

        leg2 = ComboLeg()
        leg2.conId = 636409553 # SPX 4590 P
        leg2.ratio = 1
        leg2.action = "BUY"
        leg2.exchange = "SMART"

        mycontract.comboLegs = []
        mycontract.comboLegs.append(leg1)
        mycontract.comboLegs.append(leg2)

        self.reqMktData(
            reqId=orderId,
            contract=mycontract,
            genericTickList="",
            snapshot=False,
            regulatorySnapshot=False,
            mktDataOptions=[],
        )

    # def tickOptionComputation(self, reqId: TickerId, tickType: TickType, tickAttrib: int, impliedVol: float, delta: float, optPrice: float, pvDividend: float, gamma: float, vega: float, theta: float, undPrice: float):
    #     print(f"tickOptionComputation. reqId: {reqId}, tickType: {TickTypeEnum.to_str(tickType)}, tickAttrib: {tickAttrib}, ImpVol: {impliedVol}, delta: {delta}, optPrice: {optPrice}, pvDividend: {pvDividend}, gamma: {gamma}, vega: {vega}, theta: {theta}, undPrice: {undPrice}")

    
    def tickPrice(
        self,
        reqId: TickerId,
        tickType: TickType,
        price: float,
        attrib: TickAttrib,
    ):
        # if TickTypeEnum.to_str(tickType) == "MARK_PRICE":
            print(
                "tickPrice.",
                f"reqId:{reqId}",
                f"tickType:{TickTypeEnum.to_str(tickType)}",
                f"price:{price}",
                f"attrib:{attrib}"
            )


    # def tickSize(self, reqId: TickerId, tickType: TickType, size: Decimal):
    #     if TickTypeEnum.to_str(tickType) == "LAST_SIZE":
    #         print(f"tickSize. reqId:{reqId}, tickType:{TickTypeEnum.to_str(tickType)}, size:{size}")

    # def tickGeneric(self, reqId: TickerId, tickType: TickType, value: float):
    #     print(f"tickGeneric:  reqId: {reqId}, tickType: {TickTypeEnum.to_str(tickType)}, value: {value}")

    # def tickString(self, reqId: TickerId, tickType: TickType, value: str):
    #     print("tickString: ", reqId, TickTypeEnum.to_str(tickType), value)
        
    # def tickNews(self, tickerId: int, timeStamp: int, providerCode: str, articleId: str, headline: str, extraData: str):
    #     print("tickNews",tickerId, timeStamp, providerCode, articleId, headline, extraData)

    def tickSnapshotEnd(self, reqId: int):
        print(f"tickSnapshotEnd. reqId:{reqId}")
        self.disconnect()

    def error(self, reqId: TickerId, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(reqId, errorCode, errorString, advancedOrderRejectJson)

app = TestApp()
app.connect("127.0.0.1", port, 1002)
app.run()