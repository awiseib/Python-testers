from ibapi.client import EClient
from ibapi.wrapper import EWrapper

from ibapi.protobuf.Contract_pb2 import Contract as ContractProto
from ibapi.protobuf.ContractDetails_pb2 import ContractDetails as ContractDetailsProto
from ibapi.protobuf.ContractDataRequest_pb2 import ContractDataRequest as ContractDataRequestProto


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: int):

        contractProto = ContractProto()
        contractProto.symbol = "AAPL"
        contractProto.secType = "STK"
        contractProto.exchange = "SMART"
        contractProto.currency = "USD"
        contractProto.secId = ""
        # contractProto.secIdType = ""

        contractDataRequestProto = ContractDataRequestProto()
        contractDataRequestProto.reqId = 1000
        contractDataRequestProto.contract.CopyFrom(contractProto)
        
        self.reqContractDataProtoBuf(contractDataRequestProto)

    def contractDataProtoBuf(self, contractDataProto: ContractDetailsProto):
        print(contractDataProto.contract)
        print(contractDataProto.contractDetails)

    def error(self, reqId, errorTime, errorCode, errorString, advancedOrderRejectJson=""):
        print(f"Error., Time of Error: {errorTime}, Error Code: {errorCode}, Error Message: {errorString}")

app = TestApp()
app.connect(host="127.0.0.1", port=7497, clientId=0)
app.run()