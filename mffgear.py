#!/usr/bin/env python
import json, sys, argparse, requests, os, collections

__author__  = "Jeff White [karttoon] @noottrak"
__email__   = "karttoon@gmail.com"
__version__ = "1.0.1"
__date__    = "23MAR2019"

requests.packages.urllib3.disable_warnings()

def inputCheck(msg):

    if sys.version_info[0] < 3:
        msg = raw_input(msg)
    else:
        msg = input(msg)

    return msg

def getMaster():

    url = "https://raw.githubusercontent.com/karttoon/mffgear/master/mff_master.db"

    print("\n[!] Downloading latest DB file from %s" % (url))

    data = json.loads(requests.get(url, verify=False).content)

    # Local merge
    #data = json.load(open("mff_master.db"))

    return data


def findGear(outResult, data, userResponse):

    for mffChar in data["chars"]:

        outResult[mffChar] = {}
        charGear = {}

        for gearSet in data["chars"][mffChar]["gear"]:
            charGear[gearSet] = list(data["chars"][mffChar]["gear"][gearSet])

        for gearSet in charGear:

            tempGear = list(charGear[gearSet])
            lenCheck = len(tempGear)

            for itemName in userResponse:
                if itemName in tempGear:
                    tempGear.remove(itemName)

            if len(userResponse) == 2:
                if len(tempGear) == 1 and lenCheck != 1:
                    outResult[mffChar][gearSet] = charGear[gearSet]
            else:
                if len(tempGear) == 0 and lenCheck != 0:
                    outResult[mffChar][gearSet] = charGear[gearSet]

    removeChar = []
    for mffChar, charGear in outResult.items():
        if charGear == {}:
            removeChar.append(mffChar)

    for mffChar in removeChar:
        del outResult[mffChar]

    return outResult


def buildPrint(outResult, data):

    alreadyGear = []

    printMsg = []

    # Determining print length for names
    maxLen = 0
    for mffChar in outResult:
        if len(mffChar) >= maxLen:
            maxLen = len(mffChar)

    # Loops through Tier 3 -> 1
    for i in range(3,0,-1):

        charTier = {"S": [], "A": [], "B": [], "C": [], "D": [], "?": []}

        for mffChar in outResult:

            if data["chars"][mffChar]["current"] != {}:
                alreadyGear.append(mffChar)

            if data["chars"][mffChar]["tier"] == i and data["chars"][mffChar]["current"] == {}:
                charTier[data["chars"][mffChar]["rank"]].append(mffChar)

        for tierLvl in ["S", "A", "B", "C", "D", "?"]:
            for mffChar in charTier[tierLvl]:
                gearType = list(outResult[mffChar].keys())[0]
                printMsg.append("![Tier %s | Rank %s | Gear %s] %-*s - %s" % (data["chars"][mffChar]["tier"],
                                              data["chars"][mffChar]["rank"],
                                              gearType.upper(),
                                              maxLen,
                                              mffChar,
                                              ", ".join(outResult[mffChar][gearType])))

    # Build print for candidates who already have gear defined
    if len(alreadyGear) >= 1:
        for mffChar in set(alreadyGear):

            printString = "?[Tier %s | Rank %s | Current ] %-*s - " % (data["chars"][mffChar]["tier"],
                                                                  data["chars"][mffChar]["rank"],
                                                                  maxLen,
                                                                  mffChar)

            for slotValue in data["chars"][mffChar]["current"]:
                for entry in data["chars"][mffChar]["current"][slotValue]:

                    if entry in data["defs"]["gear"]:
                        atrName = data["defs"]["gear"][entry]
                    else:
                        atrName = data["defs"]["ctp"][entry]
                    atrValue = data["chars"][mffChar]["current"][slotValue][entry]

                printString += "%s: %s, " % (atrName, atrValue)

            printMsg.append(printString[:-2])

    return printMsg


def outPrint(printMsg, args, data):

    alreadyGear = 0
    candidateGear = 0

    for count, row in enumerate(printMsg):

        if row.startswith("!"):
            if candidateGear == 0:
                print("\n[+] Candidate for Gear\n")
                candidateGear = 1
            print("[%.2d] %s " % (count + 1, row[1:]))

        if row.startswith("?"):
            if alreadyGear == 0:
                print("\n[+] Already Geared\n")
                alreadyGear = 1
            print("[%.2d] %s " % (count + 1, row[1:]))

    if args.verbose:

        userInput = inputCheck("\n[+] Enter the character number to update or Enter to skip: ")

        if userInput.isdigit():

            charPick = int(userInput) - 1

            while charPick > len(printMsg):
                print("\n[!] Not a valid pick")

            mffChar = printMsg[charPick].split("]")[1].split(" - ")[0].strip()
            data = updateChar(mffChar, data)

        else:
            print("\n[!] Skipping update process")
            pass

    else:
        print("")

    return data


def updateChar(mffChar, data):

    print("\n[+] Updating %s\n\t[-] Use format \"CRR 25\" to indicate Crit Rate 25%% or \"ENR\" for CTP of Energy\n" % (mffChar))

    for slotValue in range(1,4):

        userInput = inputCheck("Slot %s: " % (slotValue))
        gearType = userInput.split(" ")[0].upper()

        if gearType not in data["defs"]["gear"] and gearType not in data["defs"]["ctp"]:
            print("\n[!] Not a valid gear abbreviation - use `-d` flag to see defined entries")
            break

        if len(userInput.split(" ")) > 1 and userInput.split(" ")[1].isdigit():
            gearValue = int(userInput.split(" ")[1])
        else:
            gearValue = 0

        if gearType in data["defs"]["ctp"]:
            data["chars"][mffChar]["current"]["slot1"] = {gearType:0}
            break
        else:
            data["chars"][mffChar]["current"]["slot%s" % (slotValue)] = {gearType:gearValue}

    print("")
    return data


def mergeDB(data):

    mainDB = getMaster()

    newUpdate = 0

    # Update definitions for attributes/CTPs
    if mainDB["defs"] != data["defs"]:
        print("[!] Found new gear definitions")
        data["defs"] = mainDB["defs"]
        newUpdate = 1

    # Check for new chars and new gear/ranks
    for mffChar in mainDB["chars"]:

        # Correct any empty missing fields - CYA
        fields = ["all","ctp","pve","pvp"]
        for entry in fields:
            if entry not in data["chars"][mffChar]["gear"]:
                data["chars"][mffChar]["gear"][entry] = []

        # Add new chars
        if mffChar not in data["chars"]:
            print("[!] Adding new character %s" % (mffChar))
            data["chars"][mffChar] = mainDB["chars"][mffChar]
            newUpdate = 1

        # Check for rank change
        if mainDB["chars"][mffChar]["rank"] != data["chars"][mffChar]["rank"]:
            print("[!] Changing rank for %s from %s to %s" % (mffChar,
                                                              data["chars"][mffChar]["rank"],
                                                              mainDB["chars"][mffChar]["rank"]))
            data["chars"][mffChar]["rank"] = mainDB["chars"][mffChar]["rank"]
            newUpdate = 1

        # Check for gear changes
        for gearType in mainDB["chars"][mffChar]["gear"]:
            if mainDB["chars"][mffChar]["gear"][gearType] != data["chars"][mffChar]["gear"][gearType]:
                print("[!] Updating %s's %s gear to:\n%s" % (mffChar,
                                                             gearType.upper(),
                                                             json.dumps(mainDB["chars"][mffChar]["gear"][gearType], indent=4, sort_keys=True)))
                data["chars"][mffChar]["gear"][gearType] = mainDB["chars"][mffChar]["gear"][gearType]
                newUpdate = 1

    if newUpdate == 0:
        print("[!] No new updates")
    else:
        print("")

    return data


def charSetup(args, data):

    userInput = inputCheck("\n[!] Type LIST to start pick and choose for characters or Enter to roll through them all - ").upper()

    if userInput == "LIST":

        stopUpdate = 0

        listChars = []

        for mffChar in data["chars"]:
            listChars.append(mffChar)

        listChars.sort()

        # Init LIST
        for count, mffChar in enumerate(listChars):
            print("%-3s - %s" % (count + 1, mffChar))

        while stopUpdate == 0:

            userInput = inputCheck("\n[+] Enter # for character to update, \"LIST\", or \"STOP\" to exit - ").upper()

            if userInput == "STOP":
                stopUpdate = 1
                saveFile(args, data)
            elif userInput == "LIST":
                for count, mffChar in enumerate(listChars):
                    print("%-3s - %s" % (count, listChars[count]))
            else:
                if userInput.isdigit():
                    data = updateChar(listChars[int(userInput) - 1], data)
                    saveFile(args, data)

    else:

        for mffChar in data["chars"]:

            userInput = inputCheck("\n[!] Edit %s? [Y/N or Enter] - " % (mffChar)).upper()

            if userInput == "Y":

                userInput = input("\t[=] Current Tier? - ")
                data["chars"][mffChar]["tier"] = userInput

                data = updateChar(mffChar, data)

            saveFile(args, data)

    return data


def saveFile(args, data):

    writeOut = open(args.file, "w")
    writeOut.write(json.dumps(data, indent=4, sort_keys=True))
    writeOut.close()

    return


def main():

    parser = argparse.ArgumentParser(description="Script for helping find Marvel Future Fight characters to equip gear on.")
    parser.add_argument("-f", "--file", help="The file to use if not \"mff.db\".", metavar="<value>", default="mff.db")
    parser.add_argument("-m", "--merge", help="Download the latest character DB and merge it with file specified using -f flag.", action="store_true")
    parser.add_argument("-v", "--verbose", help="Prompt for gear updates when listing.", action="store_true")
    parser.add_argument("-u", "--update", help="Update your character DB with changes.", action="store_true")
    parser.add_argument("-d", "--defs", help="Print gear abbreviations", action="store_true")
    parser.add_argument("-i", "--init", help="Setup your characters for the first time.", action="store_true")
    args, unkargs = parser.parse_known_args()

    if os.path.isfile(args.file):
        data = json.load(open(args.file))
    else:
        data = getMaster()
        saveFile(args, data)

    try:

        if len(unkargs) >= 1:
            for value in unkargs[0].upper().split(","):
                if value not in data["defs"]["gear"] and value not in data["defs"]["ctp"]:
                    print("[!] Unknown gear type %s" % (value))
                    sys.exit(1)
            userResponse = unkargs[0].upper().split(",")
        else:
            userResponse = []

        if (args.defs or args.init):

            print("\n[+] Gear Abbreviations\n")
            print(json.dumps(data["defs"]["gear"], indent=4, sort_keys=True))

            print("\n[+] CTP Abbreviations\n")
            print(json.dumps(data["defs"]["ctp"], indent=4, sort_keys=True))

        if args.init:
            charSetup(args, data)

        elif args.merge:
            data = mergeDB(data)
            saveFile(args, data)

        else:
            outResult = {}
            outResult = findGear(outResult, data, userResponse)
            printMsg = buildPrint(outResult, data)
            if printMsg != []:
                data = outPrint(printMsg, args, data)
                saveFile(args, data)

    except Exception as error:

        print("\n[!] Ran into an error. Saving DB.\n%s" % (error))
        saveFile(args, data)

    return

if __name__ == '__main__':
    main()