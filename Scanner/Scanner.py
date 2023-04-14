from ibapi.client import *
from ibapi.wrapper import *
from ibapi.tag_value import *

port = 7496

global ALLCONS
ALLCONS = []

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):

        sub = ScannerSubscription()
        # sub.instrument = "FUT.US"
        sub.instrument = "STK"
        sub.locationCode = "STK.US.MAJOR"
        sub.scanCode = "HIGH_OPEN_GAP"
        # sub.abovePrice = 1
        # sub.aboveVolume = 10000
        # sub.marketCapBelow = 1000

        # Both are lists of TagValue objects: TagValue(tag, value)
        scan_options = [
            TagValue("AboveVolume", 10000),
            # TagValue("changePerc", 1),
            # TagValue("opt imp vol", 0.2),
            # TagValue("CHANGEOPENPERC","[]")
            # TagValue("colId", "55")
            # TagValue("STVOLUME_5MIN","100")
            ]
        filter_options = [
            # TagValue("marketCapAbove1e6","100000"),
            # TagValue("priceAbove", "3"),
            # TagValue("priceBelow", 1000),
            # TagValue("esgWorkforceScoreAbove", 7)
            # TagValue("changePercAbove", 0.9),
            TagValue("changePercBelow", -1),
            # TagValue("volumeAbove", 0),
            # TagValue("usdVolumeAbove", 500000),
            # TagValue("avgUsdVolumeAbove", 1000000),
            # TagValue("priceBelow", 1000),
            # TagValue("avgOptVolumeAbove", 0),
            # TagValue("excludeConvertible", 0)
            # TagValue("underConID", "495512572")
            
        ]
    
        self.reqScannerSubscription(
            reqId=123,
            subscription=sub,
            scannerSubscriptionOptions=scan_options,
            scannerSubscriptionFilterOptions=filter_options,
        )

    def scannerData(self, reqId: int, rank: int, contractDetails: ContractDetails, distance: str, benchmark: str, projection: str, legsStr: str):
        print(rank, contractDetails, distance, benchmark, projection, legsStr)


    def scannerDataEnd(self, reqId: int):
        print(f"scannerDataEnd. reqId:{reqId}")
        self.cancelScannerSubscription(reqId)
        self.disconnect
       

app = TestApp()
app.connect("127.0.0.1", port, 1001)
app.run()

print(ALLCONS)