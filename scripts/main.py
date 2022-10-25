# Python packages
from os.path import exists
from os import listdir, mkdir, rename
from requests import Session as RequestSession
from time import ctime, sleep

#import socket
#from urllib import request

# Custom packages
from log import logMessage, setupLogging

# Function to load config object
def getConfig():
    import json
    configFile = "config.json"

    try:
        if (exists(configFile) == False):
            return 2
        f = open(configFile)
        config = json.load(f)
    except:
      return 1
    return config

# main function with main loop
def main():
    # loading config
    config = getConfig()

    if (config == 1):
        print("Unexpected error while loading config, terminate")
        return
    elif (config == 2):
        print("No config file provided, terminate")
        return

    # prepare logging
    if (setupLogging(config["logDirectory"]) != 0):
        print("Unexpected error while setting up logging, terminate")
        return

    logMessage(config["logDirectory"], "Initialise watchlist")

    if (exists(config["dataDirectory"]) == False):
        try:
            mkdir(config["dataDirectory"])
        except:
            logMessage(config["logDirectory"],
                "Could not create data directory, terminate")
            return

    for item in config["watchlist"]:
        logMessage(config["logDirectory"], "Watching '" + item["title"] +
            "' under '" + item["url"] + "'")
        if (exists(config["dataDirectory"] + "/" + item["title"]) == False):
            try:
                mkdir(config["dataDirectory"] + "/" + item["title"])
            except:
                logMessage(config["logDirectory"],
                    "Could not create watcher directory, terminate")
                return

    logMessage(config["logDirectory"], "Enter main loop")

    while True:
        for item in config["watchlist"]:
            logMessage(config["logDirectory"], "Pulling " + item["title"])

            crawlerSession = RequestSession()
            # [TODO]: Get request payload from config
            request_body = {}
            response = crawlerSession.get(item["url"], data=request_body)

            if (response.ok == False):
                logMessage(config["logDirectory"], "Get request failed:\n" +
                    response.text)
                continue
            #print(response.headers)
            #print(response.cookies)

            if (exists(config["dataDirectory"] + "/" + item["title"] +
                "/snapshot") == False):
                # first snapshot
                file = open(config["dataDirectory"] + "/" +
                    item["title"] + "/snapshot", "w")
                file.write(response.text)
                file.close()
            else:
                # compare with previous snaposhot
                file = open(config["dataDirectory"] + "/" +
                    item["title"] + "/snapshot", "r")

                # [TODO]: implement content handling for Heise, Golem
                if (file.read() == response.text):
                    logMessage(config["logDirectory"], "Nothing new")
                    file.close()
                else:
                    logMessage(config["logDirectory"], "Found new content")
                    file.close()
                    # rename old snapshot
                    moveTarget = config["dataDirectory"] + "/" + item["title"] + "/snapshot_" + str(len(listdir(config["dataDirectory"] + "/" + item["title"])))
                    #print(moveTarget)
                    rename(config["dataDirectory"] + "/" + item["title"] +
                        "/snapshot", moveTarget)

                    # save new snapshot
                    file = open(config["dataDirectory"] + "/" +
                        item["title"] + "/snapshot", "w")
                    file.write(response.text)
                    file.close()

        # sleep after each round
        sleep(config["requestTimer"])
        logMessage(config["logDirectory"], "Enter next request cycle")
    return

    # [TODO]: Remove later if no longer needed
    #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #try:
    #    s.connect((config["url"], config["port"]))
    #    print("Done")
    #    s.close()
    #except:
    #    print("Failed")

    #msg=s.recv(8)
    #print(msg.decode("utf-8"))

    #return

# Call main
main()
