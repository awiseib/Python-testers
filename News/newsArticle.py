from ibapi.client import *
from ibapi.wrapper import *
import threading
import time

# Change as necessary
port = 7496


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        self.reqNewsArticle(100002, "DJNL", "DJNL$08aff51c", [])

    def newsArticle(self, requestId: int, articleType: int, articleText: str):
        print("Article Type: ", articleType)
        print( articleText)

app = TestApp()
app.connect("127.0.0.1", port, 1001)
app.run()