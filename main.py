import requests
import lxml
import pygal
import datetime

def getDateRange(start, end):
    start_date = start.split("-")
    end_date = end.split("-")
    start_date = datetime.date(int(start_date[0]), int(start_date[1]), int(start_date[2]))
    end_date = datetime.date(int(end_date[0]), int(end_date[1]), int(end_date[2]))
    delta = datetime.timedelta(days=1)
    dateRange = []

    while (start_date <= end_date):
        day = str(start_date.year) +'-'+str(start_date.month)+'-'+str(start_date.day)
        dateRange.append(day)
        start_date += delta
    return dateRange

def main():
    choice = "y"
    while choice == "y":
        symbol = input("What is the stock symbol for the company? ")
        chartType = input("What type of chart? ")
        timeSeries = input("What time series would you like to specify? ")
        startDate = input("What is the start date? Format: YYYY-MM-DD: ")
        endDate = input("what is the end date? Format: YYYY-MM-DD: ")
        dateRange = getDateRange(startDate, endDate)
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