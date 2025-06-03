from ibapi.client import *
from ibapi.common import TickerId
from ibapi.wrapper import *
from ibapi.tag_value import *

port = 7496

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):

        sub = ScannerSubscription()
        sub.instrument = "BOND"
        sub.locationCode = "BOND.US"
        sub.scanCode = "BOND_CUSIP_AZ"

        # Both are lists of TagValue objects: TagValue(tag, value)
        scan_options = []
        filter_options = [
            TagValue("marketCapAbove1e6","100000"),
            TagValue("priceAbove", 100),
            TagValue("priceBelow", 109),
            TagValue("esgWorkforceScoreAbove", 7),
            TagValue("changePercAbove", 0.9),
            TagValue("changePercBelow", -1),
            TagValue("usdVolumeAbove", 500000),
            TagValue("avgUsdVolumeAbove", 1000000),
            TagValue("priceBelow", 1000),
            TagValue("avgOptVolumeAbove", 0),
            TagValue("excludeConvertible", 0)
        ]
        self.reqScannerSubscription(orderId, sub, scan_options, filter_options)

    def scannerData(self, reqId: int, rank: int, contractDetails: ContractDetails, distance: str, benchmark: str, projection: str, legsStr: str):
        print(rank, contractDetails, distance, benchmark, projection, legsStr)


    def scannerDataEnd(self, reqId: int):
        print(f"scannerDataEnd. reqId:{reqId}")
        self.cancelScannerSubscription(reqId)
        self.disconnect()

    def error(self, reqId: TickerId, errorTime: int, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(f"Error., Time of Error: {errorTime}, Error Code: {errorCode}, Error Message: {errorString}")
        if advancedOrderRejectJson != "":
            print(f"AdvancedOrderRejectJson: {advancedOrderRejectJson}")

app = TestApp()
app.connect("127.0.0.1", port, 0)
app.run()
