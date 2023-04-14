from ibapi.client import *
from ibapi.wrapper import *
import json

port = 7496


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        # Conid 12200 == SLB Stock
        eventData = WshEventData()
        # eventData.startDate = "20210101"
        # eventData.endDate = ""
        eventData.fillCompetitors = False
        eventData.fillPortfolio = False
        eventData.fillWatchlist = False
        eventData.totalLimit = 10
        eventData.filter = '{"watchlist":["265598"],"country": "United States"}'


        # self.reqWshMetaData(orderId)
        self.reqWshEventData(orderId, eventData)

    def wshMetaData(self, reqId: int, dataJson: str):
        print("metadata.", dataJson)
        # pass

    def wshEventData(self, reqId: int, dataJson: str):
        # dataJson is a string
        # the json.loads function turns it in to a list of Dictionaries
        print("eventdata.")
        jsonDict = json.loads(dataJson)
        for i in jsonDict:
            print(i)
        self.disconnect()
        


app = TestApp()
app.connect("127.0.0.1", port, 1001)
app.run()
