import pandas as pd
import numpy as np
import pandas_datareader.data as web
import datetime as dt
import heapq
import stockViewer as sw
import sys
import os
import io
import requests

SERVER_URL = "http://127.0.0.1:5000" # server IP address (that runs in background)
CSV_EXPORTS_FOLDER_NAME = "CSV"

# read from the user a stocks key, a start and end date,
# and a letter representing a sample (D/W/M/Y) and return them as a tuple
def readStockInfo():
    key = input("enter stock symbol: ")
    startDate = input("enter start date (format must be 'yyyy/mm/dd'):")
    endDate = input("enter end date (format must be 'yyyy/mm/dd'):")
    sample = input("enter sample type (D/W/M/Y):")
    url = (SERVER_URL + "/stock/" + key)
    params = {
    'start': startDate,
    'end': endDate,
    'sample': sample
    }
    return (key, startDate, endDate, sample, url, params)

# handle the user respone from the server,
# and return the data fetched (if possible)
def handleServerResponse(url, params):
    # getting and handling response
    response = requests.get(url, params=params)
    if response.status_code == 200:
        # converting back to dataframe
        data = pd.read_json(io.BytesIO(response.content))
        return data
    else:
        print("error:", response.status_code)

# export the stock historical info dataframe into csv file
def exportDataToCSV(data, filePath):
   try:
      # create directory if it doesnt exists
      os.makedirs(os.path.dirname(filePath), exist_ok=True)
      data.to_csv(filePath, index=True, encoding='utf-8-sig', date_format='%y%m%d')
      print(f"successfully exported to: {filePath}")
   except Exception as e:
      print(f"failed to export DataFrame: {e}")

def main():
    print("type 'help' for commands list")
    # handling user input loop
    while True:
        cmd = input("$ ")
        if cmd == "osw": # handle open stock viewer command
            # reading stock info from the user and getting the url and params
            key, startDate, endDate, sample, url, params = readStockInfo()      
            # handle user respone and open stockViewer window (if possible)
            data = handleServerResponse(url, params)
            if data is not None:
                sw.openStockerViewerWindow(data, key, startDate, endDate, sample, True, True)
        elif cmd == "print":# print basic stock information
            key, startDate, endDate, sample, url, params = readStockInfo()  
            data = handleServerResponse(url, params)
            if data is not None:
                print("'" + key + "' FROM " + startDate + " TO " + endDate + " IN " + sample + " VIEW")
                print(data.to_string())
        elif cmd == "csv":# export stock historical info into a csv file
            key, startDate, endDate, sample, url, params = readStockInfo()  
            data = handleServerResponse(url, params)
            if data is not None:
                exportDataToCSV(data, CSV_EXPORTS_FOLDER_NAME+"/"+key+".csv")
        elif cmd == "help":# print commands list
            print("commands:\n"
            "'osw' for opening stock viewer window\n"
            "'print' for printing stock historical data table\n"
            "'csv' to export stock historical info into a csv file\n"
            "'exit' for closing the program")
        elif cmd == "exit":# exit command
            sys.exit()
        else:# invalid command
            print("invalid command. type 'help' for commands list")

if __name__ == "__main__":
    main()