from ibapi.client import *
from ibapi.wrapper import *
from ibapi.tag_value import *
import threading,time

port = 7496

class TestApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)


    def scannerData(self, reqId, rank, contractDetails, distance, benchmark, projection, legsStr):
        print(f"ReqId: {reqId}, Rank: {rank+1}, Contract: {contractDetails.contract}")

    def scannerDataEnd(self, reqId):
        print("Market Scanner End")
        self.cancelScannerSubscription(reqId)
        self.disconnect()

    def error(self, reqId: TickerId, errorTime: int, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(f"Error., Time of Error: {errorTime}, Error Code: {errorCode}, Error Message: {errorString}")
        if advancedOrderRejectJson != "":
            print(f"AdvancedOrderRejectJson: {advancedOrderRejectJson}")

app = TestApp()
app.connect("127.0.0.1", port, 1)
time.sleep(1)
threading.Thread(target=app.run).start()
time.sleep(1)


sub = ScannerSubscription()
sub.instrument = "STOCK.EU"
sub.locationCode = "STK.EU.AEB"
sub.scanCode = "TOP_PERC_GAIN"

scan_options = []
filter_options = [
    # TagValue("changeOpenPercAbove", 20),
    # TagValue("stVolume5minAbove", 100000),
    # TagValue("volumeAbove", 100000),
    # TagValue("priceAbove", .05),
    # TagValue("marketCapAbove1e6", 1),
    # TagValue("marketCapBelow1e6", 10000),
]
app.reqMarketDataType(3)
app.reqScannerSubscription(0, sub, scan_options, filter_options)