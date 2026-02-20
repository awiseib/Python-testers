from ibapi.client import EClient
from ibapi.wrapper import EWrapper

# Protobuf imports in order of appearance.
from ibapi.protobuf.UpdateConfigRequest_pb2 import UpdateConfigRequest as UpdateConfigRequestProto
from ibapi.protobuf.ApiConfig_pb2 import ApiConfig as ApiConfigProto
from ibapi.protobuf.ApiSettingsConfig_pb2 import ApiSettingsConfig as ApiSettingsConfigProto
from ibapi.protobuf.ApiPrecautionsConfig_pb2 import ApiPrecautionsConfig as ApiPrecautionsConfigProto
from ibapi.protobuf.UpdateConfigWarning_pb2 import UpdateConfigWarning as UpdateConfigWarningProto
from ibapi.protobuf.LockAndExitConfig_pb2 import LockAndExitConfig as LockAndExitConfigProto
from ibapi.protobuf.UpdateConfigResponse_pb2 import UpdateConfigResponse as UpdateConfigResponseProto

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
        # Initializing the larger configuration update object.
        updateConfigRequestProto = UpdateConfigRequestProto()
        updateConfigRequestProto.reqId = orderId
        
        # Reflective of the Global Configuration -> API menu
        apiConfigProto = ApiConfigProto()
        
        # Reflective of the Global Configuration -> API -> Settings menu
        apiSettingsConfigProto = ApiSettingsConfigProto()
        apiSettingsConfigProto.createApiMessageLogFile = True
        apiSettingsConfigProto.includeMarketDataInLogFile = True
        apiSettingsConfigProto.loggingLevel = "Detail"
        apiConfigProto.settings.CopyFrom(apiSettingsConfigProto)

        # Reflective of the Global Configuration -> API -> Precautions menu
        apiPrecautionsConfig = ApiPrecautionsConfigProto()
        apiPrecautionsConfig.bypassOrderPrecautions = True
        apiPrecautionsConfig.bypassPriceBasedVolatilityWarning = True
        apiConfigProto.precautions.CopyFrom(apiPrecautionsConfig)

        updateConfigRequestProto.api.CopyFrom(apiConfigProto)
        
        # Reflective of Global Configuration -> Messages
        updateConfigWarningProto = UpdateConfigWarningProto()
        updateConfigWarningProto.messageId = 520
        updateConfigWarningProto.title = "Use price management algo"
        updateConfigWarningProto.message = "Pricecap Warning Message"
        updateConfigRequestProto.acceptedWarnings.append(updateConfigWarningProto)

        '''
        # Currently appears to be non-functional - escalated with development.
        # Reflective of Global Configuration -> Lock and Exit menu
        lockAndExitProto = LockAndExitConfigProto()
        lockAndExitProto.autoLogoffTime = "11:59"
        lockAndExitProto.autoLogoffPeriod = "PM"
        lockAndExitProto.autoLogoffType = "restart"
        updateConfigRequestProto.lockAndExit.CopyFrom(lockAndExitProto)
        '''
        
        # Final request to submit updates
        self.updateConfigProtoBuf(updateConfigRequestProto)

    # Receive acknowledgement of our changes.
    def updateConfigResponseProtoBuf(self, updateConfigResponseProto: UpdateConfigResponseProto):
        print(updateConfigResponseProto)

    def error(self, reqId, errorTime, errorCode, errorString, advancedOrderRejectJson=""):
        print(f"Error., Time of Error: {errorTime}, Error Code: {errorCode}, Error Message: {errorString}")

app = TestApp()
app.connect("localhost", port, 0)
app.run()