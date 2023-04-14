from ibapi.client import *
from ibapi.wrapper import *
from ibapi.tag_value import *
from ibapi.contract import *
from ibapi.ticktype import TickTypeEnum

import threading
from time import sleep
from datetime import *


port = 7496

global globalDict
globalDict = {}

global clientId
clientId = 1001

# This is the IBAPI primary EClient and EWrapper class
class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    # Overidden error handler
    def error(self, reqId: TickerId, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        pass
        # print(reqId, errorCode, errorString, advancedOrderRejectJson)

    def nextValidId(self, orderId: int):
        self.nextOrderId = orderId

    # Returned Market Scanner information (One rank at a time)
    def scannerData(self,reqId: int,rank: int,contractDetails: ContractDetails,distance: str,benchmark: str,projection: str,legsStr: str,):
        global globalDict
        globalDict[rank] = [contractDetails.contract, "BID", "ASK", "LAST", "Today", "Yesterday", "today_CHANGE%", "prior_CHANGE%", "today_CHANGE", "prior_CHANGE"]

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

    # Returned Hisotircal Data
    def historicalData(self, reqId: int, bar: BarData):
        global globalDict
        barDate = bar.date.split()[0]
        requestedDate = startInvesting.dateCleanUp()
        
        for i in range(0,5):

            # Save Todays Bar
            if barDate == requestedDate:
                globalDict[i][4] = bar

            # Save the prior bar
            else:
                globalDict[i][5] = bar
    
    # End of All Hisotrical Data
    def historicalDataEnd(self, reqId: int, start: str, end: str):
        global clientId
        if reqId  == 4:
            clientId = self.nextOrderId
            self.disconnect()

    # Show order placed
    def openOrder(self, orderId: OrderId, contract: Contract, order: Order, orderState: OrderState):
        print(orderId, contract, order, orderState)

    def stop(self):
        self.done = True
        self.disconnect()
        
def run_loop(app_obj: TestApp):
    print("Run_Loop")
    app_obj.run()

# This is an introduction to start using threads and combining requests with one another
class startInvesting():
    # Normalize Date Values
    def dateCleanUp():
        badDate = date.today().__str__().split('-')
        goodDate = badDate[0] + badDate[1] + badDate[2]
        return goodDate

    # Create the market scanner
    def buildScanner():
        global clientId

        app = TestApp()
        app.connect("127.0.0.1", port, clientId)

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
        app.reqScannerSubscription(
            reqId=clientId,
            subscription=sub,
            scannerSubscriptionOptions=scan_options,
            scannerSubscriptionFilterOptions=filter_options,
        )
        
        app.run()
        return

    # create all historical data requests
    def buildHistorical():
        global globalDict
        app = TestApp()
        app.connect("127.0.0.1", port, clientId)
        sleep(3)
        for i in range(0,5):
            # threading.Thread(target=app.reqHistoricalData(i, globalDict[i][0], "", "2 D", "1 day", "TRADES", 1, 1, 0, [])).start()
            app.reqHistoricalData(i, globalDict[i][0], "", "2 D", "1 day", "TRADES", 1, 1, 0, [])
        app.run()

    # Create values for change values
    def calcChange():
        global globalDict
        for i in range(0,5):
            yesterday = globalDict[i][5]
            today = globalDict[i][4]
            now = globalDict[i][3]

            globalDict[i][6] = float((now / today.open)*100)
            globalDict[i][7] = float((now / yesterday.open)*100)
            globalDict[i][8] = float(now - today.open)
            globalDict[i][9] = float(now - yesterday.open)
        return

    # Place an order for the best buys
    def bestBuys():
        bestVal = globalDict[0]
        bestPerc = globalDict[0]

        # global globalDict
        for i in range(0,5):
            
            if globalDict[i][8] > bestVal[8]:
                bestVal[8] = globalDict[i][8]

            if globalDict[i][9] > bestPerc[9]:
                bestPerc[9] = globalDict[i][9]

        print(f"The largest increase by integer: {bestVal[0].symbol} by {bestVal[8]:.4f} ")
        print(f"The largest increase by percentage: {bestVal[0].symbol} by {bestVal[9]:.4f}")

        buyIt = input("Would you like to buy these? Y/N: ")
        if buyIt == "Y" or buyIt == "y":
            buyBest([bestVal, bestPerc])
        else:
            return

    # Buy the best percentage and value contracts from the bestBuys()
    def buyBest(steals):
        global clientId
        app = TestApp()
        app.connect("127.0.0.1", port, clientId)
        sleep(3)
        for i in (0, 1):
            order = Order()
            clientId+=1
            order.orderId = clientId
            order.action = "BUY"
            order.orderType = "MKT"
            order.totalQuantity = 100
            order.tif = "GTC"

            app.placeOrder(order.orderId, steals[i][0], order)
            threading.Timer(10, app.stop).start()

        app.run()
        
    # Print Scanner Results
    def printScanner():
        for i in globalDict:
            contract = globalDict[i][0]
            bidPrice = globalDict[i][1]
            askPrice = globalDict[i][2]
            lastPrice = globalDict[i][3]
            print(f"Rank: {i}; Symbol: {contract.symbol}; BID: {bidPrice}; ASK: {askPrice}; LAST: {lastPrice}")
        return

    # print top change
    def printTopDif():
        global globalDict
        print("The top 5 Orders, Compared to this morning's opening:")

        for i in range(0,5):
            symbol = globalDict[i][0].symbol
            yesterday = globalDict[i][5]
            today = globalDict[i][4]
            now = globalDict[i][3]
            

            print(f"Symbol: {symbol}; Current Price: {now} ")
            print(f"Today's bar: Open: {today.open}, High: {today.high}, Low: {today.low}, Close: {today.close};")
            print(f"{yesterday.date}'s bar: Open: {yesterday.open}, High: {yesterday.high}, Low: {yesterday.low}, Close: {yesterday.close}; ")

            print(f"Change from this morning: {globalDict[i][8]:.4f} OR {globalDict[i][6]:.4f}%.")
            print(f"Change from last trade day: {globalDict[i][9]:.4f} OR {globalDict[i][7]:.4f}%. \n")
        return


def main():
    
    startInvesting.buildScanner()

    startInvesting.printScanner()
    
    startInvesting.buildHistorical()
    
    startInvesting.calcChange()
    
    startInvesting.printTopDif()

    startInvesting.bestBuys()


if __name__ == "__main__":
    main()