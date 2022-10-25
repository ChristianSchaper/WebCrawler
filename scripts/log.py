# General import
from os.path import exists
from os import mkdir, rename
import time

# Formates message and log it into file
def logMessage(logDirectory, message = ""):
    #[TODO] Find a nice looking way to format
    message = time.ctime() + " - " +  message
    print(message)

    with open(logDirectory + "/log", "a") as myfile:
        myfile.write(message + "\n")

    return

# Ensures that the logfile exists and rename previous logs if necessary
def setupLogging(logDirectory = "log"):
    try:
        if (exists(logDirectory) == False):
            mkdir(logDirectory)
        if (exists(logDirectory + "/log") == False):
            open(logDirectory + "/log", "w")
        else:
            # [TODO] Create an archiving mechanism for old logs in case of restart
            rename(logDirectory + "/log", logDirectory + "/log_old")
            open(logDirectory + "/log", "w")
        return 0
    except:
        return 1
