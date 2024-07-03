from ibapi.client import *
from ibapi.wrapper import *
import json

port = 7496


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        self.reqWshMetaData(orderId)

    def wshMetaData(self, reqId: TickerId, data: str):
        jsonDict = json.dumps(json.loads(data), indent=2)
        open('./wshMetaData.xml', 'w').write(jsonDict)

        print("WSH Meta Data received.")

        self.disconnect()

app = TestApp()
app.connect("127.0.0.1", port, 1001)
app.run()
