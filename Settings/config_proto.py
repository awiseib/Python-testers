from ibapi.client import EClient
from ibapi.wrapper import EWrapper

from ibapi.protobuf.ConfigRequest_pb2 import ConfigRequest as ConfigRequestProto
from ibapi.protobuf.ConfigResponse_pb2 import ConfigResponse as ConfigResponseProto

port = 7496

'''
Changes come from the larger introduction of Settings Management throuh ProtoBuf.
 * For Protobuf Information, see https://www.interactivebrokers.com/campus/ibkr-api-page/protobuf-reference/#intro
 * For Function details, see https://www.interactivebrokers.com/campus/ibkr-api-page/twsapi-doc/#setting-management
'''

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: int):        
        configRequestProto = ConfigRequestProto()
        configRequestProto.reqId = orderId

        self.reqConfigProtoBuf(configRequestProto)
        

    def error(self, reqId, errorTime, errorCode, errorString, advancedOrderRejectJson=""):
        print(f"Error., Time of Error: {errorTime}, Error Code: {errorCode}, Error Message: {errorString}")


    def configResponseProtoBuf(self, configResponseProto: ConfigResponseProto):
        print(configResponseProto)


app = TestApp()
app.connect("localhost", port, 0)
app.run()