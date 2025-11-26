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
        # self.cancelScannerSubscription(reqId)
        # self.disconnect()

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
sub.numberOfRows = 10 # Displays the maximum number of scanner results. Max of 50.
sub.instrument = "STK" # Returns the Instrument type to be returned. See scannerParameters xml response for details.
sub.locationCode = "STK.US.MAJOR" # Returns the exchange regions to be returned. See scannerParameters xml response for details.
sub.scanCode = "MOST_ACTIVE" # Returns the code to sort results by. See scannerParameters xml response for details.
# sub.abovePrice = 50 # Set the maximum MARK price to filter by.
# sub.belowPrice = 55 # Set the minimum MARK price to filter by.
# sub.aboveVolume = 1000000 # Set the minimum trade volume of the day.
# sub.marketCapAbove = 100000 # Set the minimum market cap restriction  
# sub.marketCapBelow = 10000000 # Set the maximum market cap restriction. 
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
# sub.spRatingAbove = "D" # Set the minimum SP Rating
# sub.spRatingBelow = "CCC+" # set the maximum SP Rating

# sub.maturityDateAbove = "20250901" # Set the minimum Maturity date. Formatted as YYYYMMDD.
# sub.maturityDateBelow = "20360101" # Set the maximum Maturity date. Formatted as YYYYMMDD.

# sub.couponRateAbove # Set the minimum Coupon Rate
# sub.couponRateBelow # Set the maximum Coupon Rate

# sub.excludeConvertible # Determine of the bond should be convertible or not.

# sub.averageOptionVolumeAbove = 10000 # Determine the minimum average option volume from the underlying.
# # sub.scannerSettingPairs 

# sub.stockTypeFilter = "TOP_PERC_GAIN" # Determine the stock type: Common, CORP, ADR, ETF, ETN, REIT, CEF, ETMF,  EFN

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