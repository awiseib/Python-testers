from ibapi.client import *
from ibapi.wrapper import *
import threading,time



class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        print(orderId)  # Note the ID will only increment if *orders* are being placed. Otherwise the same value will be re-used.

app = TestApp()
app.connect(host="127.0.0.1", port=7497, clientId=0)
time.sleep(3)
threading.Thread(target=app.run).start()

for i in range(0,10):
    app.reqIds(-1)  # -1 should always be requested to receive a new* ID.
    time.sleep(1)
app.disconnect()