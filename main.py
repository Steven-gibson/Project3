def main():
    choice = "y"
    while choice == "y":
        symbol = input("What is the stock symbol for the company? ")
        chartType = input("What type of chart? ")
        timeSeries = input("What time series would you like to specify? ")
        startDate = input("What is the start date? Format: YYYY-MM-DD: ")
        endDate = input("what is the end date? Format: YYYY-MM-DD: ")
        # TODO: add API call and chart generation
        choice = input("Would you like to select another company? ").lower()

if __name__ == "__main__":
    main()