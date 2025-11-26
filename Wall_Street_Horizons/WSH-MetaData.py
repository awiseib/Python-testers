from ibapi.client import *
from ibapi.wrapper import *
import json

port = 7497


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        self.reqWshMetaData(orderId)

    def wshMetaData(self, reqId: TickerId, data: str):
        jsonDict = json.dumps(json.loads(data), indent=2)
        # open('./wshMetaData.xml', 'w').write(jsonDict)
        
        print("WSH Meta Data received.")
        jcon = json.loads(data)
        for jobj in jcon["meta_data"]["event_types"]:
            print(f'{jobj["name"]}: {jobj["tag"]}')
        self.disconnect()

app = TestApp()
app.connect("127.0.0.1", port, 0)
app.run()
