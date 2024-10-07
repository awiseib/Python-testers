from ibapi.client import *
from ibapi.ticktype import TickType
from ibapi.utils import Decimal
from ibapi.wrapper import *
from threading import Thread
from ibapi.ticktype import TickTypeEnum
import time

port = 7496

FUTCONTRACT = []

# request a list of contracts
class contractApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)


    def tickPrice(self, reqId: TickerId, tickType: TickType, price: float, attrib: TickAttrib):
        if TickTypeEnum.toStr(tickType) == "BID" or TickTypeEnum.toStr(tickType) == "ASK":
            print(reqId, TickTypeEnum.toStr(tickType), price, attrib)
    
    # def tickSize(self, reqId: TickerId, tickType: TickType, size: Decimal):
        # print(reqId, TickTypeEnum.toStr(tickType), size)
    
    def tickOptionComputation(self, reqId: TickerId, tickType: TickType, tickAttrib: int, impliedVol: float, delta: float, optPrice: float, pvDividend: float, gamma: float, vega: float, theta: float, undPrice: float):
        
        print(f"reqId: {reqId}, tickType: {TickTypeEnum.toStr(tickType)}, theta: {theta}, undPrice: {undPrice}")



def conidLoop(app: contractApp, conids, exchange="SMART"):
    
    reqId = 1000

    for conid in conids:
        contract = Contract()
        contract.conId = conid
        contract.exchange = exchange
        print(f"ReqId: {reqId}, ConID: {conid}")
        app.reqMktData(reqId, contract, "", False, False, [])
        reqId += 1000

if __name__ == "__main__":

    app = contractApp()
    app.connect("127.0.0.1", port, 1000)
    time.sleep(1)
    Thread(target=app.run).start()

    conids = [726474335, 726474359]
    conidLoop(app, conids)