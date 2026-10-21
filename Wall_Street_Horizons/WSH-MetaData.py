from ibapi.client import *
from ibapi.wrapper import *
import json

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

    def error(self, reqId: TickerId, errorTime: int, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(f"Error., Time of Error: {errorTime}, Error Code: {errorCode}, Error Message: {errorString}")
        if advancedOrderRejectJson != "":
            print(f"AdvancedOrderRejectJson: {advancedOrderRejectJson}")

app = TestApp()
app.connect(host="127.0.0.1", port=7497, clientId=0)
app.run()
