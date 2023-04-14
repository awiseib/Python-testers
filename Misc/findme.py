myFile = "C:\\Users\\awise\\Downloads\\api-exported-logs.txt"
newFile = "C:\\Users\\awise\\Downloads\\newFile.txt"
fileReader = []
keepers = []
keyword = "900000"

with open(myFile, "r") as api_log:
    fileReader = api_log.readlines()
    for line in fileReader:
        if keyword in line:
            linePlus = line + "\n"
            keepers.append(linePlus)

with open(newFile, "w") as nf:
    for nl in keepers:
        nf.write(nl)