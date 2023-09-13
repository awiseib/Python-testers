from ibapi.client import *
from ibapi.wrapper import *
import json

port = 7497


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        eventData = WshEventData()
        # eventData.conId = "12200"
        # eventData.startDate = "20100101"
        # eventData.endDate = ""
        eventData.fillCompetitors = False
        eventData.fillPortfolio = False
        eventData.fillWatchlist = False
        eventData.totalLimit = 100
        eventData.filter = '{"watchlist":["12200"],"country": "All", "wshe_ed": "true", "wshe_bod": "true"}'

        """
        Filters pulled from wshMetaData. Look for section header in response to find filter name.
        String(Boolean) is only acceptable value to include.

        wshe_bod    ==  Board of Directors
        wshe_ed     ==  Earnings Dates
        wshe_div    ==  Dividend Dates
        """
        self.reqWshEventData(orderId, eventData)

    def wshEventData(self, reqId: int, dataJson: str):
        print("eventdata.")
        jsonDict = json.dumps(json.loads(dataJson), indent=2)
        print(jsonDict)


app = TestApp()
app.connect("127.0.0.1", port, 1001)
app.run()
