import requests
import time
import csv
import xml.etree.ElementTree as ET

# Update these to YOUR environment.
csvPath = 'D:\\Downloads\\Trades.csv'

# Flex Web Serivce is only availble for LIVE accounts.
# This example uses the trust test account.
# Because the trust account is Read-Only, no contents will show besides the header

# 1. Build your flex query in Client Portal
# 2. Right click the page, click "Inspect"
# 3. Go to Network tab
# 4. You will see a Data response -> In the "entries" section, you will find the "queryId" field with the corresponding value

requestBase = "https://www.interactivebrokers.com/Universal/servlet/FlexStatementService.SendRequest?"
token = "t=656530010732398240553724" # Valid 2023-03-01, 10:13:43 EST — 2024-01-31, 10:13:43 EST
queryId = "&q=771568"
version = "&v=3"

# 5. Combine requestUrl, queryId, tokenId, and include version 3
requestUrl = "".join([requestBase, token, queryId, version])
# Example: https://www.interactivebrokers.com/Universal/servlet/FlexStatementService.SendRequest?t=174034019902345466159208&q=771568&v=3

# 6. Create a GET request for that URL
flexReq = requests.get(url=requestUrl)

# Read XML
tree = ET.ElementTree(ET.fromstring(flexReq.text))
root = tree.getroot()

# 7. If <Status> received is "Success", you have begun the process
# 8. You will need to use the <Url> and <ReferenceCode> value to retrieve the value

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


# 9. Combine your new url, reference code, and your previous token and version number

receiveUrl = "".join([receiveBase, "?",token, refCode, version])
# Example: https://gdcdyn.interactivebrokers.com/Universal/servlet/FlexStatementService.GetStatement?t=174034019902345466159208&q=5773202049&v=3

# Pause for sample
print("Hold for Request.")
time.sleep(10)

# 10. Generate a GET request for the new URL
receiveUrl = requests.get(url=receiveUrl, allow_redirects=True)

# 11. CSV value returned
open(csvPath, 'wb').write(receiveUrl.content)


print("Done!")