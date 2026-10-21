from ibapi.client import *
from ibapi.wrapper import *


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        self.reqUserInfo(
            reqId=orderId
        )

    def userInfo(self, reqId, whiteBrandingId):
        print(f"User Info. WhiteBrandID: {whiteBrandingId}")
    

    def error(self, reqId: TickerId, errorTime: int, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(f"Error., Time of Error: {errorTime}, Error Code: {errorCode}, Error Message: {errorString}")
        if advancedOrderRejectJson != "":
            print(f"AdvancedOrderRejectJson: {advancedOrderRejectJson}")
        
if __name__ == "__main__":
    app = TestApp()
    app.connect(host="127.0.0.1", port=7497, clientId=0)
    app.run()