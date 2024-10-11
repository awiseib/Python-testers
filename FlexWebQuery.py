import requests
import json
import csv
import time
import xml.etree.ElementTree as ET
import pprint

# Update these to YOUR environment.
# Please note this sample assumes you are using CSV formatting, though the only change will be in writing to your file.
csvPath = "./sample.csv"

# Flex Web Serivce is only availble for LIVE accounts.
# This example uses the trust test account.
# Because the trust account is Read-Only, no contents will show besides the header

# 1. Build your flex query in Client Portal. 
# 2. Click the Info button to the left of your Flex Query
# 3. Copy the "Query ID" under Activity Flex Query Details

requestBase = "https://ndcdyn.interactivebrokers.com/AccountManagement/FlexWebService"
token = 528191644107458877539776
queryId = 1080086
flex_version = 3

# List of response headers to print (all others discarded)
RESP_HEADERS_TO_PRINT = ["Content-Type", "Content-Length", "Date", "Set-Cookie", "User-Agent"]

def pretty_request_response(resp: requests.Response) -> str:
    """Print request and response legibly."""
    req = resp.request
    rqh = '\n'.join(f"{k}: {v}" for k, v in req.headers.items())
    rqh = rqh.replace(', ', ',\n    ')
    rqb = f"\n{pprint.pformat(json.loads(req.body))}\n" if req.body else ""
    try:
        rsb = f"\n{pprint.pformat(resp.json())}\n" if resp.text else ""
    except json.JSONDecodeError:
        rsb = resp.text
    rsh = '\n'.join([f"{k}: {v}" for k, v in resp.headers.items() if k in RESP_HEADERS_TO_PRINT])
    return_str = '\n'.join([
        80*'-',
        '-----------REQUEST-----------',
        f"{req.method} {req.url}",
        rqh,
        f"{rqb}",
        '-----------RESPONSE-----------',
        f"{resp.status_code} {resp.reason}",
        rsh,
        f"{rsb}\n",
    ])
    return return_str

send_slug = "/SendRequest"

send_params = {
    "t":token, 
    "q":queryId, 
    "v":flex_version
}

# 5. Create a GET request for that URL
try:
    flexReq = requests.get(url=requestBase+send_slug, params=send_params)
    print(pretty_request_response(flexReq))
except Exception as e:
    print("Request failed with exception: %s" % {e})
    
# Read XML
tree = ET.ElementTree(ET.fromstring(flexReq.text))
root = tree.getroot()

# 6. If <Status> received is "Success", you have begun the process
# 7. You will need to use the <Url> and <ReferenceCode> value to retrieve the value

for child in root:
    if child.tag == "Status":
        if child.text != "Success":
            print(f"Failed to generate Flex statement. Stopping...")
            exit()
    elif child.tag == "ReferenceCode":
        refCode = child.text


# Pause for sample
print("Hold for Request.")
time.sleep(20)

receive_slug = "/GetStatement"
receive_params = {
    "t":token, 
    "q":refCode, 
    "v":flex_version
}

# 9. Generate a GET request for the new URL
receiveUrl = requests.get(url=requestBase+receive_slug, params=receive_params, allow_redirects=True)
print(pretty_request_response(receiveUrl))
# 10. CSV value returned
open(csvPath, 'wb').write(receiveUrl.content)


print("Done!")