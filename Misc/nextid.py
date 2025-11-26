from ibapi.client import *
from ibapi.wrapper import *
import threading,time

port = 7497


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        print(orderId)

app = TestApp()
app.connect("127.0.0.1", port, 0)
time.sleep(3)
threading.Thread(target=app.run).start()
app.reqIds(-1)