from ibapi.client import *
from ibapi.wrapper import *

port = 7496


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        self.reqNewsProviders()

    # Subscribed news sources are delivered here after reqNewsProviders
    def newsProviders(self, newsProviders: ListOfNewsProviders):
        print(
            "newsProviders:\n\t"+ 
            '\n\t'.join(f'{provider.code}: {provider.name}' for provider in newsProviders)
        )
        self.disconnect()

    def error(self, reqId: TickerId, errorTime: int, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(f"Error., Time of Error: {errorTime}, Error Code: {errorCode}, Error Message: {errorString}")
        if advancedOrderRejectJson != "":
            print(f"AdvancedOrderRejectJson: {advancedOrderRejectJson}")

app = TestApp()
app.connect("127.0.0.1", port, 10)
app.run()
