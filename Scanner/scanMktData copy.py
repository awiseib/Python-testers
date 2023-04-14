from ibapi.client import *
from ibapi.wrapper import *
from ibapi.tag_value import *
from ibapi.contract import *
from ibapi.ticktype import TickTypeEnum

import threading
from time import sleep
from datetime import datetime


port = 7496

global globalDict
globalDict = {}

global clientId
clientId = 0


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)        

    def nextValidId(self, orderId: int):
        global clientId
        sub = ScannerSubscription()
        sub.instrument = "STK"
        sub.locationCode = "STK.US.MAJOR"
        sub.scanCode = "TOP_OPEN_PERC_GAIN"

        # Both are lists of TagValue objects: TagValue(tag, value)
        scan_options = []
        filter_options = [
            TagValue("volumeAbove", "10000"),
            TagValue("marketCapBelow1e6", "1000"),
            TagValue("priceAbove", "1"),
        ]
        sleep(3)
        # Request my Market Scanner
        self.reqScannerSubscription(
            reqId=clientId,
            subscription=sub,
            scannerSubscriptionOptions=scan_options,
            scannerSubscriptionFilterOptions=filter_options,
        )
        clientId +=1
        run=True
        while run:
            if len(globalDict) <= 49:
                sleep(1)
            else:
                run=False
        for i in globalDict:
            contract = globalDict[i][0]
            bidPrice = globalDict[i][1]
            askPrice = globalDict[i][2]
            lastPrice = globalDict[i][3]
            print(f"Rank: {i}; Symbol: {contract.symbol}; BID: {bidPrice}; ASK: {askPrice}; LAST: {lastPrice}")
        print("EOF")
        
    def error(self, reqId: TickerId, errorCode: int, errorString: str):
        pass

    # Returned Market Scanner information (One rank at a time)
    def scannerData(self,reqId: int,rank: int,contractDetails: ContractDetails,distance: str,benchmark: str,projection: str,legsStr: str,):
        global globalDict
        globalDict[rank] = [contractDetails.contract, "BID", "ASK", "LAST"]

    # End of market scanner
    def scannerDataEnd(self, reqId: int):
        # Cancel lingering market scanner
        self.cancelScannerSubscription(reqId)

        # Request market data for all of our scanner values.
        for rank in globalDict:
            x = threading.Thread(target=self.reqMktData(reqId=rank,contract=globalDict[rank][0],genericTickList="",snapshot=True,regulatorySnapshot=False,mktDataOptions=[]))
            x.start()

    # Returned market data
    def tickPrice(self, reqId: TickerId, tickType: TickType, price: float, attrib: TickAttrib):
        global globalDict
        for ind,value in enumerate(globalDict[reqId]):
            if TickTypeEnum.to_str(tickType) == value:
                globalDict[reqId][ind] = price


    # End of all market data request
    def tickSnapshotEnd(self, reqId: int):
        if reqId == 49:
            # After my last request, disconnect from socket.
            self.disconnect()

    def historicalData(self, reqId: int, bar: BarData):
        print(f"historicalData. Contract: {globalDict[reqId][0].symbol}, Open: {bar.open}, Low: {bar.low}, High: {bar.high}, Close: {bar.close}.")

    # def historicalDataEnd(self, reqId: int, start: str, end: str):
        # self.disconnect()


def main():
    app = TestApp()
    app.connect("127.0.0.1", port, 1001)
    app.run()

if __name__ == "__main__":
    main()