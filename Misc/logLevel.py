from ibapi.client import *
from ibapi.wrapper import *
import threading
import time

port = 7496


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def logRequest(self, fnName, fnParams):
        print(f"fnName: {fnName}\nfnParams: {fnParams}")

    def error(self, reqId: TickerId, et, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(reqId, errorCode, errorString, advancedOrderRejectJson)


app = TestApp()
app.connect("127.0.0.1", port, 0)
time.sleep(1)
threading.Thread(target=app.run).start()
time.sleep(1)

for i in range(0,5):
    app.setServerLogLevel(i)
    time.sleep(1)