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
        print(reqId, TickTypeEnum.toStr(tickType), price, attrib)
    
    def tickSize(self, reqId: TickerId, tickType: TickType, size: Decimal):
        print(reqId, TickTypeEnum.toStr(tickType), size)


def main():

    contract = Contract()
    contract.conId = 265598
    contract.exchange = "SMART"

    app = contractApp()
    app.connect("127.0.0.1", port, 1000)
    time.sleep(1)
    Thread(target=app.run).start()
    
    app2 = contractApp()
    app2.connect("127.0.0.1", port, 2000)
    time.sleep(1)
    Thread(target=app2.run).start()
    
    time.sleep(1)
    
    app.reqMktData(1000, contract, "", False, False, [])
    app2.reqMktData(2000, contract, "", False, False, [])

    time.sleep(10)

    app.disconnect()


if __name__ == "__main__":
    main()