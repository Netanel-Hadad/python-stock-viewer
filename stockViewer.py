import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

plt.style.use('default')

WINDOW_TITLE = "Stock Viewer"
XLABEL = 'Date'
YLABEL = 'Price'
UP_CANDLE_COLOR = 'green'
DOWN_CANDLE_COLOR = 'red'
DATE_INDEX_LABEL_ROTATION_ANGLE = 45
MAX_AMOUNT_OF_X_AXIS_TICKS = 30
VOLUME_MAX_Y_VALUE = 500000000

# this function recives a stocks dataframe containing its info, 
# the stock's key, a start and end date, and a sample,
# and creates and opens a candle stick graph of the given stock
def openStockerViewerWindow(data, key, startDate, endDate, sample, showMountainLine, showVolumeBars):
   
   # create a figure and set the window title and info
   fig, ax = plt.subplots()
   fig.canvas.manager.set_window_title(WINDOW_TITLE)
   plt.xlabel(XLABEL)
   plt.ylabel(YLABEL)
   plt.title("'" + key + "' FROM " + startDate + " TO " + endDate + " IN " + sample + " VIEW")
   plt.grid(axis='y')

   # acording to the sample the user has choosen, set the date format, interval and candles width
   # width of candlestick scales acording to choosen view sample
   if sample == 'D':
      inter = 1
      dateFormat = '%y/%m/%d'
      width = 0.8
      width2 = .1
   elif sample == 'W':
      inter = 7
      dateFormat = '%y/%m'
      width = 2.5
      width2 = .65
   elif sample == 'M':
      inter = 30
      dateFormat = '%y/%m'
      width = 15
      width2 = 3
   elif sample == 'Y':
      inter = 365
      dateFormat = '%y/%m'
      width = 15
      width2 = 3

   # format the date acording to the sample
   fig.gca().xaxis.set_major_formatter(mdates.DateFormatter(dateFormat))
   # change the tick interval acodring to the sample
   fig.gca().xaxis.set_major_locator(mdates.DayLocator(interval=inter))
   # puts x-axis labels on an angle
   fig.gca().xaxis.set_tick_params(rotation=30)

   # set x-axis range when first opening the window
   plt.xlim([pd.Timestamp(startDate), pd.Timestamp(endDate)]) 

   # up and down prices
   up = data[data.Close>=data.Open]
   down = data[data.Close<data.Open]

   #plot up prices
   ax.bar(up.index,up.Close-up.Open,width,bottom=up.Open,color=UP_CANDLE_COLOR)
   ax.bar(up.index,up.High-up.Close,width2,bottom=up.Close,color=UP_CANDLE_COLOR)
   ax.bar(up.index,up.Low-up.Open,width2,bottom=up.Open,color=UP_CANDLE_COLOR)

   #plot down prices
   ax.bar(down.index,down.Close-down.Open,width,bottom=down.Open,color=DOWN_CANDLE_COLOR)
   ax.bar(down.index,down.High-down.Open,width2,bottom=down.Open,color=DOWN_CANDLE_COLOR)
   ax.bar(down.index,down.Low-down.Close,width2,bottom=down.Close,color=DOWN_CANDLE_COLOR)

   #rotate x-axis tick labels
   plt.xticks(rotation=DATE_INDEX_LABEL_ROTATION_ANGLE, ha='right')

   # set the max amount of ticks on the x axis so labels wont hide each other
   ax.xaxis.set_major_locator(plt.MaxNLocator(MAX_AMOUNT_OF_X_AXIS_TICKS))

   # draw mountain line, line that connects all the close prices values
   if showMountainLine:
      ax.plot(data.index[:], data['Close'], '-', label="Close")
      ax.legend()

   volumeBarWidth = 0.8

   # creating the Volume bars
   if showVolumeBars:
      ax2 = ax.twinx()
      ax2.bar(data.index, data['Volume'], volumeBarWidth, color='grey')
      # when choosing a value for 'VOLUME_MAX_Y_VALUE',
      # we choose a value that will make the bars stay at the lower bottom of the graph
      ax2.set_ylim(0, VOLUME_MAX_Y_VALUE)
      ax2.yaxis.set_visible(False)

   fig.tight_layout()
   plt.show()