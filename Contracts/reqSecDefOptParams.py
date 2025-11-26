from ibapi.client import *
from ibapi.wrapper import *
from datetime import datetime

port = 7496


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):

        self.reqSecDefOptParams(  
            reqId=123,
            underlyingSymbol="ROG",
            futFopExchange="",  
            underlyingSecType="STK",
            underlyingConId="762280415",
        )

    def securityDefinitionOptionParameter(
        self,
        reqId: int,
        exchange: str,
        underlyingConId: int,
        tradingClass: str,
        multiplier: str,
        expirations: SetOfString,
        strikes: SetOfFloat,
    ):
        print(
            "securityDefinitionOptionParameter.",
            f"reqId:{reqId}",
            f"exchange:{exchange}",
            f"underlyingConId:{underlyingConId}",
            f"tradingClass:{tradingClass}",
            f"multiplier:{multiplier}",
            f"expirations:{expirations}",
            f"strikes:{strikes}",
        )

    def securityDefinitionOptionParameterEnd(self, reqId: int):
        print(f"securityDefinitionOptionParameterEnd. reqId:{reqId}")

    def error(self, reqId: TickerId, errorTime: int, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(f"Error., Time of Error: {errorTime}, Error Code: {errorCode}, Error Message: {errorString}")
        if advancedOrderRejectJson != "":
            print(f"AdvancedOrderRejectJson: {advancedOrderRejectJson}")

app = TestApp()
app.connect("127.0.0.1", port, 0)
app.run()
