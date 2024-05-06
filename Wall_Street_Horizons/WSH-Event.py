from ibapi.client import *
from ibapi.wrapper import *
import json

port = 7496


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        eventData = WshEventData()
        # eventData.conId = 265598
        # eventData.startDate = "20100101"
        # eventData.endDate = ""
        # eventData.fillCompetitors = False
        # eventData.fillPortfolio = False
        # eventData.fillWatchlist = False
        # eventData.totalLimit = 100
        eventData.filter = '{"watchlist":["265598"],"country": "All", "wshe_ed": "true", "wshe_div": "true"}'

        """
        Filters pulled from wshMetaData. Look for section header in response to find filter name.
        String(Boolean) is only acceptable value to include.

        wshe_bod    ==  Board of Directors
        wshe_ed     ==  Earnings Dates
        wshe_div    ==  Dividend Dates
        wshe_eps    ==   
        wshe_cc     ==
        wshe_option ==
        wshe_sec    == 
        wshe_qe     ==  Quarterly Earnings
        wshe_ic     ==
        wshe_sh     == 
        """
        self.reqWshEventData(orderId, eventData, 173)

    def wshEventData(self, reqId: int, dataJson: str):
        print("eventdata.")
        jsonDict = json.dumps(json.loads(dataJson), indent=4)
        print(jsonDict)
        self.disconnect()


app = TestApp()
app.connect("127.0.0.1", port, 1001)
app.run()
