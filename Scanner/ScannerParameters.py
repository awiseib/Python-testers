from ibapi.client import *
from ibapi.wrapper import *

port = 7496


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        self.reqScannerParameters()

    def scannerParameters(self, xml: str):
        open('./scanParams.xml', 'w').write(xml)
        print("ScannerParameters received.")

app = TestApp()
app.connect("127.0.0.1", port, 1001)
app.run()