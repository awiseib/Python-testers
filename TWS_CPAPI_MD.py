# Library Imports

# CPAPI
import requests
import time
import urllib3
import json
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# TWS API
from ibapi.client import *
from ibapi.wrapper import *
import csv
from datetime import datetime
import threading
from ibapi.ticktype import TickTypeEnum

port = 7496
acctId = "DU257590" # NCHIN054

SPY_CONID = "625037597" # SPY 412 C 20230424
QQQ_CONID = "625036837" # QQQ 315 C 20230424
CSV_HOLSTER = "D:\\Code\\comparison.csv"

# 55,31,71,70,7635,84,86,87
# Symbol, Last, Low, High, Mark, Bid, Ask, Volume,


PRICE_TRACKER = {}

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)
        self.nextOrderId = 1
        self.contract = (0, Contract())

    def nextValidId(self, orderId: OrderId):
        self.nextOrderId = orderId

    def tickPrice(self, reqId: TickerId, tickType: TickType, price: float, attrib: TickAttrib):
        tick = TickTypeEnum.to_str(tickType)
        request = PRICE_TRACKER[reqId][1]
        if tick in request:
            request[tick] = float(price)

    def error(self, reqId: TickerId, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(errorCode, errorString, advancedOrderRejectJson)



def marketDataFeed(app: TestApp, contracts: list):
    for contract in contracts:
        app.nextOrderId += 1

        PRICE_TRACKER[app.nextOrderId] = (contract,{"Symbol":0,"LAST":0,"LOW":0,"HIGH":0,"MARK":0,"BID":0,"ASK":0,"VOLUME":0})
        app.reqMktData(app.nextOrderId, contract, "232", False, False, [])


def stop_app(app: TestApp):
    # Kill app after 1 hour
    time.sleep(3600)
    app.disconnect()
    exit()

def cpApiMktData(conid):

    md_url = "".join(["https://localhost:5000/v1/api/iserver/marketdata/snapshot?conids=",conid, "&fields=55,31,71,70,7635,84,86,87"])
    requests.get(url = md_url, verify=False)
    mdResponse = requests.get(url = md_url, verify=False)
    return mdResponse

def dataComparison():
    for contract in PRICE_TRACKER:
        coninfo = PRICE_TRACKER[contract][1]
    

    csvFile = open(CSV_HOLSTER, 'a', newline='')
    csvWriter = csv.writer(csvFile, delimiter=',')
    csvWriter.writerow(["Source", "Datetime", "ConID", "Symbol","LAST","LOW","HIGH","MARK_PRICE","BID","ASK","VOLUME"])
    csvFile.close()

    while True:
        for contract in PRICE_TRACKER:
            cpapiData = cpApiMktData(PRICE_TRACKER[contract][0].conId)

            coninfo = PRICE_TRACKER[contract][1]
            mycon = PRICE_TRACKER[contract][0]

            cpJson = json.loads(cpapiData.text)[0]
            cpList = ["CPAPI", datetime.now(), mycon.conId, cpJson["55"], cpJson["31"], cpJson["71"], cpJson["70"], cpJson["7635"], cpJson["84"], cpJson["86"], cpJson["87"]]

            csvFile = open(CSV_HOLSTER, 'a', newline='')
            csvWriter = csv.writer(csvFile, delimiter=',')
            csvWriter.writerow( ["TWSAPI", datetime.now(), mycon.conId, cpJson["55"], coninfo['LAST'], coninfo['LOW'], coninfo['HIGH'], coninfo['MARK'], coninfo['BID'], coninfo['ASK'], coninfo['VOLUME'] ] )
            csvWriter.writerow(cpList)
            csvWriter.writerow('')
            csvFile.close()


        time.sleep(2)

def main():
        
    app = TestApp()
    app.connect("127.0.0.1", port, 1001)
    time.sleep(3)
    app_obj = threading.Thread(target=app.run)
    app_obj.start()


    spyCon = Contract()
    spyCon.conId = SPY_CONID
    spyCon.exchange = "SMART"

    qqqCon = Contract()
    qqqCon.conId = QQQ_CONID
    qqqCon.exchange = "SMART"

    contracts = [spyCon, qqqCon]

    # This creates a background feed of live market data
    marketDataFeed(app, contracts)

    dataComparison()
    
    # Kills the app after 1 hour
    stop_app(app)
    

if __name__ == "__main__":
    main()