# Python 10.35.1 Upgrade Instructions
## Purpose
With the introduction of TWSAPI 10.35.1, Interactive Brokers has begun shifting our API offering to include the [Google Protocol Buffers](https://protobuf.dev/) (Protobuf) to help with data serialization. 
The inclusion of Protobuf will allow Interactive Brokers and our clients to expand our software into new programming languages through popular standards. 
While the new features are exciting, we have observed that Python requires some additional steps regarding setup that clients should look to follow. 

Interactive Brokers is actively working to improve the file installation to automate this process. Though for now, the steps mentioned below wold otherwise need to be modified manually.

## Files To Be Modified In Python Source:
 * setup.py
 * ibapi/client.py
 * ibapi/decoder.py
 * ibapi/protobuf/Contract_pb2.py
 * ibapi/protobuf/ExecutionDetails_pb2.py
 * ibapi/protobuf/ExecutionRequest_pb2.py
 
## Setup.py
We would need to first modify the setup.py file used to install the API at `{TWS API}/source/pythonclient/setup.py`.
1. Modify line 17 to reference `packages=["ibapi","ibapi/protobuf"],` to include our ibapi/protobuf directory.
2. Insert a new line after 17 for `install_requires=["protobuf"],` to automatically install the protobuf libray.
3. Save the file.

## ibapi/client.py
Next we would need to modify our client.py file saved at `{TWS API}/source/pythonclient/ibapi/client.py`.
1. On line 145, we will need to include `ibapi.` prior to our protobuf reference.
   The final line should appear as `from ibapi.protobuf.ComboLeg_pb2 import ComboLeg as ComboLegProto`
2. We will do the same for line 146, `from ibapi.protobuf.ExecutionFilter_pb2 import ExecutionFilter as ExecutionFilterProto`.
3. And again on line 147, `from ibapi.protobuf.ExecutionRequest_pb2 import ExecutionRequest as ExecutionRequestProto`
4. Save the file.

## ibapi/decoder.py
Identical to client.py, we'll need to reference the ibapi.protobuf file rather than the google.protobuf file.
1. Include `ibapi.` on line 33 prior to the protobuf reference.
	Our final line should appear as `from ibapi.protobuf.ExecutionDetails_pb2 import ExecutionDetails as ExecutionDetailsProto`.
2. We'll do the same on line 34 for `from ibapi.protobuf.ExecutionDetailsEnd_pb2 import ExecutionDetailsEnd as ExecutionDetailsEndProto`.
3. Save the file.

## ibapi/protobuf/Contract_pb2.py
Again, we wil reference ibapi.protobuf rather than a direct protobuf package.
1. On line 25, we'll prepend the value to `ibapi.protobuf.` rather than as the direct package reference.
	The final line 25 should appear as `import ibapi.protobuf.ComboLeg_pb2 as ComboLeg__pb2`.
2. We will do the same on line 26, `import ibapi.protobuf.DeltaNeutralContract_pb2 as DeltaNeutralContract__pb2`.
3. Save the file.

## ibapi/protobuf/ExecutionDetails_pb2.py
We will again prepend `ibapi.protobuf.`. 
1. We'll first modify line 25, to show `import ibapi.protobuf.Contract_pb2 as Contract__pb2`.
2. We will do the same for line 26, `import ibapi.protobuf.Execution_pb2 as Execution__pb2`.
3. Save the file.

## ibapi/protobuf/ExecutionRequest_pb2.py
And for the final time, we can prepend `ibapi.protobuf.`.

## Installing the updated version.
Once all 6 files have been updated, we will need to run the setup.py script to update the python interpreter. 
The process to update the interpretter is the same as what is mentioned in the [documentation](https://www.interactivebrokers.com/campus/ibkr-api-page/twsapi-doc/#setup-python).
1. Navigate to `{TWS API}/source/pythonclient` through your terminal. 
2. Run `python setup.py install` then press the return key. After a few moments, ibapi will update with our new files and should no longer cause an error.

# Protobuf UserWarning messages
After resolving the reference errors, using the TWSAPI may print a UserWarning upon connection. These warnings are predominantly cosmetic and can be ignored.
These issues are caused by the Pypi release of protobuf running version 6.30.1 and above, while the TWS API is built with 5.29.3.
The warning is simply notifying users that their version is 1 major version different. However, given protobuf is currently backgwards compatible, this should not
present any issues with the implementation. 
Developers uncomfortable with the warning messages have a few options:
1. [Recompile Protobuf](https://protobuf.dev/getting-started/pythontutorial/) against their [Github 5.29.3 version](https://github.com/protocolbuffers/protobuf/tree/v5.29.3) to maintain parity with the TWS API implementations.
2. Users can also modify the code source, linked by the protobuf warning, and simply remove lines 94 and on from the runtime_version.py file. 
