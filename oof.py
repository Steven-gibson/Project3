import requests
import lxml
import pygal
import datetime
import sys
import math


# below function takes user input date start and end
# gets every date in between them, inclusive
# has check for what user defined (weekly, monthly, etc.)

def getDateRange(start, end, timeSeries):
    print("The start date is", start)
    start_date = start.split("-")
    end_date = end.split("-")
    start_date = datetime.date(int(start_date[0]), int(start_date[1]), int(start_date[2]))
    end_date = datetime.date(int(end_date[0]), int(end_date[1]), int(end_date[2]))
    dateRange = []
    # if timeSeries == "INTRADAILY":
    #     delta = datetime.timedelta(days=1)
    #     while (start_date <= end_date):
    #         day = str(start_date.year) +'-'+str(start_date.month)+'-'+str(start_date.day)
    #         dateRange.append(day)
    #         start_date += delta
    #     return dateRange
    if timeSeries == "DAILY":
        delta = datetime.timedelta(days=1)
        while (start_date <= end_date):
            day = str(start_date.year) +'-'+str(start_date.month)+'-'+str(start_date.day)
            dateRange.append(day)
            start_date += delta
        return dateRange
    elif timeSeries == "WEEKLY":
        delta = datetime.timedelta(weeks=1)
        while (start_date <= end_date):
            day = str(start_date.year) +'-'+str(start_date.month)+'-'+str(start_date.day)
            dateRange.append(day)
            start_date += delta
        return dateRange
    elif timeSeries == "MONTHLY":
        #delta = datetime.timedelta(months=1)
        while (start_date <= end_date):
            day = str(start_date.year) +'-'+str(start_date.month)+'-'+str(start_date.day)
            dateRange.append(day)
            start_date += delta
        return dateRange

def getInput():
    inputs = []
    while True:
        symbol = input("\nWhat is the stock symbol for the company? ")
        inputs.append(symbol)
        while True:
            try:
                chartType = int(input("\nWhat type of chart?\n1. Bar\n2. Line\nSelection: "))
                if chartType == 1 or chartType == 2:
                    inputs.append(chartType)
                    break
                else:
                    print("Your options are 1 or 2")
                    continue
            except:
                print("Enter numbers 1 or 2 only")
                continue
        while True:
            try:
                timeSeries = int(input("\nWhat time series would you like to specify?\n1. Intraday\n2. Daily\n3. Weekly\n4. Monthly\nSelection: "))
                if timeSeries == 1 or timeSeries == 2 or timeSeries == 3 or timeSeries == 4:
                    inputs.append(timeSeries)
                    break
                else:
                    print("Your options are 1, 2, 3, or 4")
                    continue
            except:
                print("Enter numbers 1-4 only")
                continue
        while True:
            try:
                start_Date = input("\nWhat is the start date? Format: YYYY-MM-DD: ")
                start_Date = str(datetime.datetime.strptime(start_Date, "%Y-%m-%d"))
                startDate = start_Date.split(' ')[0]
                break
            except ValueError:
                print('Please enter according to format')

        inputs.append(startDate)

        while True:
            try:
                end_Date = input("\nWhat is the end date? Format: YYYY-MM-DD: ")
                end_Date = str(datetime.datetime.strptime(end_Date, "%Y-%m-%d"))
                endDate = end_Date.split(' ')[0]
                break
            except ValueError:
                print('Please enter according to format')

        inputs.append(endDate)
        return inputs

def apiCall(timeSeries, symbol):
    if timeSeries == "DAILY":
        # https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=GOOGL&outputsize=full&apikey=TJ5UI0CUVXDLAV9K
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_' + timeSeries + '&symbol='+ symbol +'&outputsize=full&interval=5min&apikey=TJ5UI0CUVXDLAV9K'
        r = requests.get(url)
        data = r.json()
    return data

def parseJSON(rawJSON, timeSeries, dateRange):
    
    if timeSeries == "DAILY":
        dicts = rawJSON['Time Series (Daily)']
        dates, opens, highs, lows, closes = [], [], [], [], []
        for date in dicts:
            dates.append(datetime.datetime.strptime(date, '%Y-%m-%d'))
            opens.append(float(dicts[date]['1. open']))
            highs.append(float(dicts[date]['2. high']))
            lows.append(float(dicts[date]['3. low']))
            closes.append(float(dicts[date]['4. close']))
    jsonDateRange = [dates, opens, highs, lows, closes]
    return jsonDateRange

        #for date in dateRange:
        #    try:
         #       splitDate = date.split('-')
          #      day = date.split('-')[2].zfill(2)
           #     date = splitDate[0] +'-'+splitDate[1]+'-'+ day
            #    jsonDateRage.append(rawJSON['Time Series (Daily)'][date])
            #except KeyError:
             #   continue
        #return jsonDateRage


def createGraph(jsonDateRange,timeSeries): #jsonDateRange = dates[], opens[], highs[], lows[], closes[]
    # TODO append date range to title as well
    # TODO capture lowest and highest range in the data so can use map()

    #categories = list(jsonDateRange[0].keys())
    #print('*')
    #print(categories)

    if timeSeries == "DAILY":
        #title = "Time Series (Daily)"


        line_chart = pygal.Line()
        line_chart.title = "Time Series (Daily) " #+ jsonDateRange[0][0] + " to " +  jsonDateRange[0][-1]
        line_chart.x_labels = map(str, range(int(jsonDateRange[0][0].strftime('%d')), int(jsonDateRange[0][-1].strftime('%d'))))
        line_chart.add('Open', [None, None, jsonDateRange[1]])
        line_chart.add('High', [None, None, None, None, None, None, jsonDateRange[2]])
        line_chart.add('Low', [jsonDateRange[3]])
        line_chart.add('Close', [jsonDateRange[4]])
        line_chart.render()

    #minimum = 9999999
    #maximum = 0
    #for entry in jsonDateRange:
    #    if float(entry['3. low']) < minimum:
    #        minimum = float(entry['3. low'])
    #print("min is", minimum)
    #for entry in jsonDateRange:
    #    if float(entry['2. high']) > maximum:
    #        maximum = float(entry['2. high'])
    #print("max is", maximum)
    #line_chart = pygal.Line()
    #line_chart.title = title
    #line_chart.y_labels = map(str, range(math.floor(minimum), math.ceil(maximum)))
    #line_chart.add(categories[0], [None, None,    0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
    #line_chart.add(categories[1],  [None, None, None, None, None, None,    0,  3.9, 10.8, 23.8, 35.3])
    #line_chart.add(categories[2],      [85.8, 84.6, 84.7, 74.5,   66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
    #line_chart.add(categories[3],  [14.2, 15.4, 15.3,  8.9,    9, 10.4,  8.9,  5.8,  6.7,  6.8,  7.5])
    #line_chart.add(categories[4],  [14.2, 15.4, 15.3,  8.9,    9, 10.4,  8.9,  5.8,  6.7,  6.8,  7.5])
    #line_chart.render_in_browser()

def main():
    choice = "y"
    timeSeriesChoice = {1: "INTRADAILY",2:"DAILY",3:"WEEKLY",4:"MONTHY"}
    while choice == "y":
        inputs = getInput()
        dateRange = getDateRange(inputs[3], inputs[4],timeSeriesChoice[inputs[2]])
        #inputs[0-4] = symbol, chartType, timeSeries, startDate, endDate

        data = apiCall(timeSeriesChoice[inputs[2]],inputs[0])
        jsonDateRange = parseJSON(data, timeSeriesChoice[inputs[2]],dateRange)
        createGraph(jsonDateRange, timeSeriesChoice[inputs[2]])
        choice = input("\nWould you like to select another company? ").lower()

        #print(data["Monthly Time Series"]["2022-10-20"])
        

if __name__ == "__main__":
    main()
