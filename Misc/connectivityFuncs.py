from ibapi.client import *
from ibapi.wrapper import *

import threading, time

port = 7496
class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)
        self.req_count = 0
    
    def connectAck(self):
        print("API Connected.")

    def connectionClosed(self):
        print("API Disconnected.")
    
    def symbolSamples(self, reqId, contractDescriptions):
        print(reqId, contractDescriptions)
    
    def error(self, reqId, errorTime, errorCode, errorString, advancedOrderRejectJson=""):
        print(reqId, errorTime, errorCode, errorString, advancedOrderRejectJson)

if __name__ == '__main__':
    app = TestApp()
    # app.setConnectOptions("+PACEAPI")
    app.connect("127.0.0.1", 7496, 0)
    time.sleep(1)
    threading.Thread(target=app.run).start()
    time.sleep(1)
    # print(app.connectOptions)
    # time.sleep(3)
    # app.disconnect()
    while True:
        app.reqMatchingSymbols(app.req_count, "AAPL")
        app.req_count += 1