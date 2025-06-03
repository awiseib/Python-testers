from ibapi.client import *
from ibapi.common import TickerId
from ibapi.wrapper import *
from ibapi.tag_value import *

port = 7496

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)
    
    def nextValidId(self, orderId: TickerId):
        '''
        Support Scan Codes:
            HIGH_OPT_IMP_VOLAT
            LOW_OPT_IMP_VOLAT
            TOP_OPT_IMP_VOLAT_GAIN
            TOP_OPT_IMP_VOLAT_LOSE
            HIGH_OPT_IMP_VOLAT_OVER_HIST
            LOW_OPT_IMP_VOLAT_OVER_HIST
            OPT_VOLUME_MOST_ACTIVE
            OPT_OPEN_INTEREST_MOST_ACTIVE
            HIGH_OPT_VOLUME_PUT_CALL_RATIO
            LOW_OPT_VOLUME_PUT_CALL_RATIO
            HIGH_OPT_OPEN_INTEREST_PUT_CALL_RATIO
            LOW_OPT_OPEN_INTEREST_PUT_CALL_RATIO
            HOT_BY_OPT_VOLUME
        '''
        scan_code = "HIGH_OPT_IMP_VOLAT"

        # This would be the expected layout when requesting StockOptions
        stk_opt_sub = ScannerSubscription()
        stk_opt_sub.instrument = "STK"
        stk_opt_sub.locationCode = "STK.US.MAJOR"
        stk_opt_sub.scanCode = scan_code

        # This would be the expected layout when requesting Index Options
        ind_opt_sub = ScannerSubscription()
        ind_opt_sub.instrument = "IND.US"
        ind_opt_sub.locationCode = "IND.US"
        ind_opt_sub.scanCode = scan_code

        # We are using the same Scan and Filter options for both scanners
        scan_options = []

        filter_options = [
            TagValue("hasOptionsIs", "true")
        ]

        app.reqScannerSubscription(orderId, stk_opt_sub, scan_options, filter_options)

    def scannerData(self, reqId: int, rank: int, contractDetails: ContractDetails, distance: str, benchmark: str, projection: str, legsStr: str):
        print(f"Rank: {rank+1}, Contract: {contractDetails.contract}")


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