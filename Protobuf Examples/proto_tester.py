from google.protobuf import text_format
from ibapi.client import *
from ibapi.wrapper import *
import ibapi.protobuf.ApiConfig_pb2
import ibapi.protobuf.ConfigRequest_pb2

api_descriptor = ibapi.protobuf.ApiConfig_pb2._globals
config_descriptor = ibapi.protobuf.ConfigRequest_pb2._globals
updateConifg_descriptor = ibapi.protobuf.UpdateConfigRequest_pb2._globals

for k,v in api_descriptor.items():
    print(f'{k}: {v}\n') 

attrs = vars(api_descriptor["ApiConfig"])
for k,v in attrs.items():
    print(f'{k}: {v}\n')

print(text_format.MessageToString(api_descriptor["_APICONFIG"]))

print("### Descriptor Items ###")
for k,v in config_descriptor.items():
    print(f'{k}: {v}\n')

print("### Attributes ###")
attrs = vars(config_descriptor["ConfigRequest"])
for k,v in attrs.items():
    print(f'{k}: {v}\n')

print("### Descriptor ###")
print(text_format.MessageToString(config_descriptor["ConfigRequest"]))


print("### Descriptor Items ###")
for k,v in updateConifg_descriptor.items():
    print(f'{k}: {v}\n')

print("### Attributes ###")
attrs = vars(updateConifg_descriptor["UpdateConfigRequest"])
for k,v in attrs.items():
    print(f'{k}: {v}\n')


print("### Descriptor Items ###")
for k,v in updateConifg_descriptor.items():
    print(f'{k}: {v}\n')

print("### Attributes ###")
attrs = vars(updateConifg_descriptor["ApiConfig"])
for k,v in attrs.items():
    print(f'{k}: {v}\n')
