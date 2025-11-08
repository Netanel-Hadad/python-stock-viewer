import pandas as pd
import numpy as np
import pandas_datareader.data as web
import datetime as dt
import heapq
import stockViewer as sw

ONE_YEAR_ROI_COLUMN_NAME = "1-Y-ROI"
DAYS_IN_YEAR = 365
DAYS_IN_52_WEEKS = 52 * 7
FIFTHY_TWO_WEEKS_HIGH_COLUMN_NAME = "52 Weeks High"
FIFTHY_TWO_WEEKS_LOW_COLUMN_NAME = "52 Weeks Low"

def main():

   # ---------- handling user input ---------- #

   key = input("enter stock symbol: ")
   startDate = input("enter start date (format must be 'yyyy/mm/dd'):")
   endDate = input("enter end date (format must be 'yyyy/mm/dd'):")
   sample = input("enter sample type (D/W/M/Y):")

   # ---------- data and calculations ---------- #

   # fetch data
   data = web.DataReader(key, 'stooq', start=startDate, end=endDate)

   # calculate and add 1 year ROI column
   # we calculate and add the ROI before resampling because doing it afterwards will not work (causes empty values).
   currentCloseRow = data['Close']
   oneYearCloseRow = currentCloseRow.shift(periods=-DAYS_IN_YEAR)
   data[ONE_YEAR_ROI_COLUMN_NAME] = round((currentCloseRow - oneYearCloseRow) / oneYearCloseRow * 100, 2)

   # calculate and add the 52 Weeks High/Low rows
   # we loop through the data and add the high and low values into max and min heaps
   # after 52 weeks (in data rows) we start adding the 52 Week High/Low values by using the heaps
   # and removing the values from the unneceseary day (that after 52 weeks in days, is no longer in that time range)
   maxHeap = []
   minHeap = []
   counter = 0 # current row index in numbers
   for index, row in data.iterrows(): 
      if counter < DAYS_IN_52_WEEKS:
         heapq.heappush(maxHeap, -data.at[data.index[counter], 'High'])
         heapq.heappush(minHeap, data.at[data.index[counter], 'Low'])
      else: # counter >= 52
         # adding 52 weeks high value
         data.at[data.index[counter - DAYS_IN_52_WEEKS], FIFTHY_TWO_WEEKS_HIGH_COLUMN_NAME] = -maxHeap[0]
         maxHeap.remove(-data.at[data.index[counter - DAYS_IN_52_WEEKS], 'High'])
         heapq.heappush(maxHeap, -data.at[data.index[counter], 'High'])
         # adding 52 weeks low value
         data.at[data.index[counter - DAYS_IN_52_WEEKS], FIFTHY_TWO_WEEKS_LOW_COLUMN_NAME] = minHeap[0]
         minHeap.remove(data.at[data.index[counter - DAYS_IN_52_WEEKS], 'Low'])
         heapq.heappush(minHeap, data.at[data.index[counter], 'Low'])

      counter += 1

   # ---------- resmapling data ---------- #

   # resample to daily/weekly/monthly/yearly data, taking the last day of each week/month/year
   data = data.resample(sample).last()
   # for some reason resampling reverse the order of the dataframe, so sort is needed
   data = data.sort_values(by='Date', ascending=False)

   # ---------- output ---------- #

   #print("'" + key + "' FROM " + startDate + " TO " + endDate + " IN " + sample + " VIEW")
   #print(data)

   sw.openStockerViewerWindow(data, key, startDate, endDate, sample, True, True)

if __name__ == "__main__":

   main()
