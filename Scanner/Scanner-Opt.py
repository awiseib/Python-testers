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
        sub.instrument = "STK"
        sub.locationCode = "STK.US.MAJOR"
        sub.scanCode = "TOP_PERC_GAIN"

        # Both are lists of TagValue objects: TagValue(tag, value)
        scan_options = [
            TagValue("hasOptionsIs", True)
            ]
        filter_options = [
            TagValue("priceAbove", 10000),
            TagValue("priceBelow", 10000),
            TagValue("optVolumeAbove", 10000),
            # TagValue("optVolumeBelow", 109),
            
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
        self.disconnect()

    def error(self, reqId: TickerId, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(reqId, errorCode, errorString, advancedOrderRejectJson)
       

app = TestApp()
app.connect("127.0.0.1", port, 1001)
app.run()
