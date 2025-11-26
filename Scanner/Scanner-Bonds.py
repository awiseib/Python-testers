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
        sub.locationCode = "BOND.WW"
        sub.scanCode = "HIGH_BOND_ASK_YIELD_ALL"
        '''
        Moody ratings scale:
        Investment Grade
        Aaa: Highest quality, minimal credit risk
        Aa1, Aa2, Aa3: High quality, very low credit risk
        A1, A2, A3: Upper-medium grade, low credit risk
        Baa1, Baa2, Baa3: Medium grade, moderate credit risk

        Speculative Grade (High Yield/Junk)
        Ba1, Ba2, Ba3: Speculative elements, substantial credit risk
        B1, B2, B3: Speculative, high credit risk
        Caa1, Caa2, Caa3: Poor standing, very high credit risk
        Ca: Highly speculative, likely in or very near default
        C: Lowest rated, typically in default
        '''
        # sub.moodyRatingAbove = "C" # Minimum Moody Rating
        # sub.moodyRatingBelow = "Caa1" # Maximum Moody Rating

        '''
        ## Currently spRatings are flagged as disabled
        Standard & Poor's (S&P) uses a letter-based rating system to evaluate the creditworthiness of bonds and debt issuers, ranging from highest quality to default:

        Investment Grade
        AAA: Highest rating, extremely strong capacity to meet financial commitments
        AA+, AA, AA-: Very strong capacity to meet financial commitments
        A+, A, A-: Strong capacity to meet financial commitments, somewhat susceptible to economic conditions
        BBB+, BBB, BBB-: Adequate capacity to meet financial commitments, more subject to adverse economic conditions

        Speculative Grade (High Yield/Junk)
        BB+, BB, BB-: Less vulnerable in the near-term but faces major ongoing uncertainties
        B+, B, B-: More vulnerable to adverse business or economic conditions
        CCC+, CCC, CCC-: Currently vulnerable and dependent on favorable conditions to meet commitments
        CC: Highly vulnerable; default has not yet occurred but is expected
        C: Highly vulnerable; default proceedings have been initiated
        D: Payment default on a financial commitment
        '''
        sub.spRatingAbove = "CCC" # Set the minimum SP Rating
        sub.spRatingBelow = "AAA" # set the maximum SP Rating

        # Both are lists of TagValue objects: TagValue(tag, value)
        scan_options = []
        filter_options = [
            # TagValue("marketCapAbove1e6","100000"),
            # TagValue("priceAbove", 100),
            # TagValue("priceBelow", 109),
            # TagValue("esgWorkforceScoreAbove", 7),
            # TagValue("changePercAbove", 0.9),
            # TagValue("changePercBelow", -1),
            # TagValue("usdVolumeAbove", 500000),
            # TagValue("avgUsdVolumeAbove", 1000000),
            # TagValue("priceBelow", 1000),
            # TagValue("avgOptVolumeAbove", 0),
            # TagValue("excludeConvertible", 0)
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
