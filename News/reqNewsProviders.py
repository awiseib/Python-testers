from concurrent.futures import thread
from ibapi.client import *
from ibapi.wrapper import *
import threading

# Change as necessary
port = 7496


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        self.reqNewsProviders()

    # Subscribed news sources are delivered here after reqNewsProviders
    def newsProviders(self, newsProviders: ListOfNewsProviders):
        print(
            "newsProviders.",
            f"newsProviders:{newsProviders}",
        )


app = TestApp()
app.connect("127.0.0.1", port, 1001)
app.run()
