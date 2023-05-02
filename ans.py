import json


#This will create a Final_Output_File.txt which is wanted as per the gievn challenge.
def textWriter(listOfDict):
    with open("Final_Output_File.txt", 'w') as f: 
        for i in listOfDict:
            for key, value in i.items(): 
                f.write('%s:%s\n' % (key, value))
            f.write("\n----------------------------------------------\n\n")
    f.close()



#Divided the given listofDict to two lists based on start session and end session.
#Then sorted them based on ID and merged them to create a summarized dictionary.
def convertTwoLists(listofDict):
    startLists = []
    endLists = []
    finalListOfDict = []
    for i in listofDict:
        tempLists = i.values()
        if  "START" in tempLists:
            startLists.append(i)
        else:
            endLists.append(i)
    sorted(startLists, key=lambda i: i['id'])
    sorted(endLists, key=lambda i: i['id'])
    for i in range(len(startLists)):
        startDict = startLists[i]
        endDict = endLists[i]

        tempDict = {}
        tempDict["Session-ID"] = startDict["id"]
        tempDict["Session-Start-Time"] = int(startDict["timestamp"])
        tempDict["Session-End-Time"] = int(endDict["timestamp"])
        tempDict["Duration"] = tempDict["Session-End-Time"] - tempDict["Session-Start-Time"]
        if(tempDict["Duration"] > 86400):
            tempDict["Car-Returned-after-24HRS"] = "true"
        else:
            tempDict["Car-Returned-after-24HRS"] = "false"
        if(endDict["comments"] == ""):
            tempDict["Car-Was-Damaged"] = "false"
        else:
            tempDict["Car-Was-Damaged"] = "true"
        finalListOfDict.append(tempDict)
        print(tempDict)

    return finalListOfDict #return the summarized dictionary.
    



def convertStringToDict(listOfJSON):
    listOfDict = []
    for string in listOfJSON:
        tempDict = json.loads(string)
        listOfDict.append(tempDict)
    return listOfDict



def captureJSON(f):
    listOfJSON = []
    tempString = ""
    state = 0
    for line in f: #used Finite state machines concept to parse the string and get the exact JSON embeddings which is wanted.
        if "{" in line and state==0:
            tempString += "{"
            state=1
        elif state==1:
            tempString += line
            if "}" in line:
                tempString = tempString.split("}")[0]
                tempString += "}"
                listOfJSON.append(tempString)
                tempString = ""
                state = 0
    res = []
    for sub in listOfJSON:
        res.append(sub.replace("\n", ""))
    return res


#Main Function to do all the operations
def fileOpening():
    FILENAME = input("Enter the File Name: ")
    f = open(FILENAME, "r")
    listOfJSON = captureJSON(f)#Function to convert JSON based strings to List of JSON based strings.
    listOfDict = convertStringToDict(listOfJSON)#Function to convert JSON based strings to Dictionaries.
    finalMergedDict = convertTwoLists(listOfDict)#Function to create a summarized dictionary to print it in .txt file format.
    textWriter(finalMergedDict)#Function to write the summarized dictionary to a .txt file.
    f.close()



if __name__ == "__main__":
    fileOpening()
