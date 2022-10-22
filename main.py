import requests
import lxml
import pygal
import datetime
import sys

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
        symbol = input("What is the stock symbol for the company? ")
        inputs.append(symbol)
        while True:
            try:
                chartType = int(input("What type of chart?\n1. Bar\n2. Line\nSelection: "))
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
                timeSeries = int(input("What time series would you like to specify?\n1. Intraday\n2. Daily\n3. Weekly\n4. Monthly\nSelection: "))
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
                start_Date = input("What is the start date? Format: YYYY-MM-DD: ")
                start_Date = str(datetime.datetime.strptime(start_Date, "%Y-%m-%d"))
                startDate = start_Date.split(' ')[0]
                break
            except ValueError:
                print('Please enter according to format')

        inputs.append(startDate)

        while True:
            try:
                end_Date = input("what is the end date? Format: YYYY-MM-DD: ")
                end_Date = str(datetime.datetime.strptime(end_Date, "%Y-%m-%d"))
                endDate = end_Date.split(' ')[0]
                break
            except ValueError:
                print('Please enter according to format')

        inputs.append(endDate)
        return inputs

def main():
    choice = "y"
    timeSeriesChoice = {1: "INTRADAILY",2:"DAILY",3:"WEEKLY",4:"MONTHY"}
    while choice == "y":
        inputs = getInput()
        dateRange = getDateRange(inputs[3], inputs[4],timeSeriesChoice[inputs[2]])
        print(dateRange)
        # TODO: add API call and chart generation
        choice = input("Would you like to select another company? ").lower()
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_' + timeSeries.upper() + '&symbol='+ symbol +'&interval=5min&apikey=TJ5UI0CUVXDLAV9K'
        #url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=TJ5UI0CUVXDLAV9K'
        r = requests.get(url)
        data = r.json()
        print(data["Monthly Time Series"]["2022-10-20"])

if __name__ == "__main__":
    main()