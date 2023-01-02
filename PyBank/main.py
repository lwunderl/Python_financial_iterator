import sys
import csv

def main():
    #ensure command line criteria is met
    if len(sys.argv) != 3:
        print("Must have 3 arguments: program.py file.csv file.txt")
        sys.exit()
    elif is_valid_pyfile(sys.argv[0]) and is_valid_csvfile(sys.argv[1]):
        #create dictionary of csv file
        try:
            data = read_data(sys.argv[1])
        except KeyError:
            print(".csv format/header is incorrect, you may have the wrong .csv file")
        else:
            #total months from csv dictionary
            total_months = len(data)
            #net change from csv dictionary
            profit_net_total = profit_net_change(data)
            #create a profit monthly change dictionary from csv dictionary
            profit_difference = profit_monthly_change(data)
            #calculate average of monthly change dictionary
            average_change = profit_average_change(profit_difference)
            #greatest increase from monthly change dictionary
            best_profit = greatest_increase(profit_difference)
            #greatest decrease from monthly change dictionary
            worst_profit = greatest_decrease(profit_difference)
            #print analysis to terminal
            print(
                f"\nFinancial Analysis\n"
                f"------------------------------------\n"
                f"Total Months: {total_months}\n"
                f"Total: ${profit_net_total:,}\n"
                f"Average Change: ${average_change:,.2f}\n"
                f"Greatest Increase in Profits: {best_profit['month']} ${best_profit['monthly_change']:,.2f}\n"
                f"Greatest Decrease in Profits: {worst_profit['month']} ${worst_profit['monthly_change']:,.2f}\n"
                )
            #write analysis file
            with open(sys.argv[2], "w") as file:
                file.write(
                    f"Financial Analysis\n"
                    f"------------------------------------\n"
                    f"Total Months: {total_months}\n"
                    f"Total: ${profit_net_total:,.2f}\n"
                    f"Average Change: ${average_change:,.2f}\n"
                    f"Greatest Increase in Profits: {best_profit['month']} ${best_profit['monthly_change']:,.2f}\n"
                    f"Greatest Decrease in Profits: {worst_profit['month']} ${worst_profit['monthly_change']:,.2f}"
                    )

def is_valid_pyfile(sysarg):
    try:
        path, extention = sysarg.split(".")
    except ValueError:
        print("Must have valid file extention: .py")
        sys.exit()
    else:
        if extention == "py":
            return True
        else:
            print("Only .py file allowed")
            sys.exit()

def is_valid_csvfile(sysarg):
    try:
        path, extention = sysarg.split(".")
    except ValueError:
        print("Must have valid file extention: .csv")
        sys.exit()
    else:
        if extention == "csv":
            return True
        else:
            print("Only .csv file allowed")
            sys.exit()

def read_data(r):
    #read data in csv file and save to dictionary
    data = []
    with open(r,"r",newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append({"date": row["Date"], "profit": row["Profit/Losses"]})
    return data

def profit_net_change(n):
    #calculate net change on read data dictionary
    profit_net_change = 0
    for _ in n:
        profit_net_change = float(_["profit"]) + profit_net_change
    return profit_net_change

def profit_monthly_change(m):
    #create monthly change dictionary from read data dictionary
    monthly_change_list = []
    monthly_change = m[0].get("profit")
    for _ in m[1:]:
        monthly_change = float(_["profit"]) - float(monthly_change)
        monthly_change_list.append({"month": _["date"], "monthly_change": monthly_change})
        monthly_change = _["profit"]
    return monthly_change_list

def profit_average_change(a):
    #calculate average of monthly change dictionary
    monthly_change_total = 0
    for _ in a:
        monthly_change_total = float(_["monthly_change"]) + monthly_change_total
    return monthly_change_total / len(a)

def greatest_increase(i):
    #find largest monthly increase
    greatest_increase = 0
    increase_month = "month"
    for _ in i:
        if _["monthly_change"] > greatest_increase:
            greatest_increase = _["monthly_change"]
            increase_month = _["month"]
    return {"month": increase_month, "monthly_change": greatest_increase}

def greatest_decrease(d):
    #find largest monthly decrease
    greatest_decrease = 0
    decrease_month = "month"
    for _ in d:
        if _["monthly_change"] < greatest_decrease:
            greatest_decrease = _["monthly_change"]
            decrease_month = _["month"]
    return {"month": decrease_month, "monthly_change": greatest_decrease}

if __name__ == "__main__":
    main()