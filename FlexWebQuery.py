import requests
import time
import csv
import xml.etree.ElementTree as ET

# Update these to YOUR environment.
csvPath = 'D:\\Downloads\\custFlex.xml'

# Flex Web Serivce is only availble for LIVE accounts.
# This example uses the trust test account.
# Because the trust account is Read-Only, no contents will show besides the header

# 1. Build your flex query in Client Portal
# 2. Click the Info button to the left of your Flex Query
# 3. Copy the "Query ID" under Activity Flex Query Details

requestBase = "https://www.interactivebrokers.com/Universal/servlet/FlexStatementService.SendRequest?"
# token = "t=220638997034176155165000" # Valid 2023-03-01, 10:13:43 EST — 2024-01-31, 10:13:43 EST
# queryId = "&q=771568"

token = "t=468323735188770213387953" # csdem9545
queryId = "&q=800969" # Trades Flex Query

version = "&v=3"

# 4. Combine requestUrl, queryId, tokenId, and include version 3
requestUrl = "".join([requestBase, token, queryId, version, "&period=LastQuarter&noOfDays=100"])
# Example: https://www.interactivebrokers.com/Universal/servlet/FlexStatementService.SendRequest?t=174034019902345466159208&q=771568&v=3

# 5. Create a GET request for that URL
flexReq = requests.get(url=requestUrl)

# Read XML
tree = ET.ElementTree(ET.fromstring(flexReq.text))
root = tree.getroot()

# 6. If <Status> received is "Success", you have begun the process
# 7. You will need to use the <Url> and <ReferenceCode> value to retrieve the value

for child in root:
    if child.tag == "Status":
        if child.text != "Success":
            print("Failed to request")
            print(child)
            break
    elif child.tag == "ReferenceCode":
        refCode = "&q="+child.text
    elif child.tag == "Url":
        receiveBase = child.text
    else:
        print(child.tag, ":", child.text)


# 8. Combine your new url, reference code, and your previous token and version number

receiveUrl = "".join([receiveBase, "?",token, refCode, version])
# Example: https://gdcdyn.interactivebrokers.com/Universal/servlet/FlexStatementService.GetStatement?t=174034019902345466159208&q=5773202049&v=3

# Pause for sample
print("Hold for Request.")
time.sleep(20)

# 9. Generate a GET request for the new URL
receiveUrl = requests.get(url=receiveUrl, allow_redirects=True)

# 10. CSV value returned
open(csvPath, 'wb').write(receiveUrl.content)


print("Done!")