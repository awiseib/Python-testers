from ibapi.client import *
from ibapi.wrapper import *
from datetime import datetime
from ibapi.ticktype import TickTypeEnum
import time
import threading

port = 7496
acctId = "DU5240685"

# Will be used to organize market data

PRICE_TRACKER = {}
ACCOUNT_INFO = {}

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)
        self.nextOrderId = 1
        self.contract = (0, Contract())

    def nextValidId(self, orderId: OrderId):
        self.nextOrderId = orderId

    def contractDetails(self, reqId: int, contractDetails: ContractDetails):
        self.contract = (reqId, contractDetails.contract)

    def tickPrice(self, reqId: TickerId, tickType: TickType, price: float, attrib: TickAttrib):
        tick = TickTypeEnum.toStr(tickType)
        request = PRICE_TRACKER[reqId][1]
        if tick in request:
            request[tick] = float(price)
    
    def updateAccountValue(self, key: str, val: str, currency: str, accountName: str):
        if key == "CashBalance":
            ACCOUNT_INFO[key] = float(val)

    def updatePortfolio(self, contract: Contract, position: Decimal, marketPrice: float, marketValue: float, averageCost: float, unrealizedPNL: float, realizedPNL: float, accountName: str):
        ACCOUNT_INFO[contract.localSymbol] = {"contract":contract,"position": float(position), "marketPrice": marketPrice, "marketValue": marketValue, "averageCost": averageCost}

    def openOrder(self, orderId: OrderId, contract: Contract, order: Order, orderState: OrderState):
        print(f"openOrder. orderId: {orderId}, contract: {contract}, order: {order}")
    
    def execDetails(self, reqId: int, contract: Contract, execution: Execution):
        print(f"execDetails. reqId: {reqId}, contract: {contract}, execution: {execution}")

    def error(self, reqId: TickerId, errorTime: int, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(f"Error., Time of Error: {errorTime}, Error Code: {errorCode}, Error Message: {errorString}")
        if advancedOrderRejectJson != "":
            print(f"AdvancedOrderRejectJson: {advancedOrderRejectJson}")


def buildContracts(app: TestApp, tickers: list):
    
    reqId = 300
    contracts = []
    for symbol in tickers:

        contract = Contract()
        contract.symbol = symbol
        contract.secType = "STK"
        contract.exchange = "SMART"
        contract.currency = "USD"

        app.reqContractDetails(reqId, contract)
        requested = True

        while requested:
            if app.contract[0] == reqId:
                contracts.append(app.contract[1])
                requested = False
                reqId += 1

    return contracts

def marketDataFeed(app: TestApp, contracts: list):
    for contract in contracts:
        app.nextOrderId += 1

        PRICE_TRACKER[app.nextOrderId] = (contract,{"BID":0,"ASK":0,"LAST":0})
        app.reqMktData(app.nextOrderId, contract, "", False, False, [])

def portfolioMonitor(app:TestApp):
    # This was built for a single account in mind. 
    # This could be easily built out to accomodate a mutli-account structure similar to the marketDataFeed method.
    app.reqAccountUpdates(True, acctId)

def tradeStrategy(app: TestApp):
    # Set up "oldX" for each contract
    for contract in PRICE_TRACKER:
            coninfo = PRICE_TRACKER[contract][1]
            coninfo["oldlast"] = coninfo["LAST"]
            coninfo["oldbid"] = coninfo["BID"]
            coninfo["oldask"] = coninfo["ASK"] 


    order = Order()
    order.orderType = "LMT"
    order.totalQuantity = 5
    order.tif = "DAY"
    order.outsideRth = True

    while True:
        for contract in PRICE_TRACKER:
            coninfo = PRICE_TRACKER[contract][1]
            mycon = PRICE_TRACKER[contract][0]
            app.nextOrderId+=1

            # We only want to buy a contract if we have more than $10000.
            if  ACCOUNT_INFO["CashBalance"] >= 10000:
                # Our 'mastermind' strategy
                if (coninfo["BID"] > (coninfo["oldbid"] + 0.02) and (coninfo["ASK"] + 0.02) > coninfo["oldask"]) or coninfo["LAST"] > (coninfo["oldlast"] + 0.02):

                    order.action = "BUY"
                    order.lmtPrice = coninfo["BID"]
                    
                    app.placeOrder(app.nextOrderId, PRICE_TRACKER[contract][0], order)
                
            # We only want to sell if we have position - we do not want to short in this scenario.
            try:
                if ACCOUNT_INFO[mycon.symbol]["position"] >= 10:
                    if (coninfo["BID"] < (coninfo["oldbid"] - 0.02) and (coninfo["ASK"] - 0.02) < coninfo["oldask"]) or coninfo["LAST"] < (coninfo["oldlast"] - 0.02):

                        order.action = "Sell"
                        order.lmtPrice = coninfo["ASK"]
                        
                        app.placeOrder(app.nextOrderId, PRICE_TRACKER[contract][0], order)
                
                coninfo["oldlast"] = coninfo["LAST"]
                coninfo["oldbid"] = coninfo["BID"]
                coninfo["oldask"] = coninfo["ASK"]
            except KeyError:
                pass


        time.sleep(5)

def stop_app(app: TestApp):
    # Kill app after 10 minutes
    time.sleep(600)
    app.disconnect()
    exit()

def main():

    app = TestApp()
    app.connect("127.0.0.1", port, 0)
    time.sleep(3)
    app_obj = threading.Thread(target=app.run)
    app_obj.start()

    portfolioMonitor(app)
    # Put what contracts you wish to auto-trade here.
    tickers = ["AAPL", "NVDA", "F", "GE"]
    contracts = buildContracts(app, tickers)

    # This creates a background feed of live market data
    marketDataFeed(app, contracts)

    # Not necessary, but I wanted to be sure we could start all data feeds before moving on
    time.sleep(5)

    trd_obj = threading.Thread(target=tradeStrategy, args=(app,))
    trd_obj.start()

    
    # Kills the app after 10 minutes
    stop_app(app)
    

if __name__ == "__main__":
    main()