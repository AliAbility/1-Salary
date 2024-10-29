from operator import index
import pandas as pd
import csv
from datetime import datetime
from fontTools.misc.plistlib import end_date
from  Data_Entry import Get_amount,Get_category,Get_date,Get_description
import matplotlib.pyplot as plt


class CSV:
    CSV_FILE = "finance_data.csv"
    COLUMNS = ["date", "amount", "category", "description"]
    FORMAT = "%d-%m-%Y"
    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)
    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description

        }
        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
        print("Entry Added Successfully")
    @classmethod
    def get_transactions(cls,start_date,end_date):
        df = pd.read_csv(cls.CSV.CSV_FILE)
        df ["date"] = pd.to_datetime(df.date)
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")

        mask = (["date"] >= start_date) & (df["date"] <= end_date)
        filtered_df = df.loc[mask]
        if filtered_df.empty:
            print("No Transactions Found")
        else:
            print(f"Transactions from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}")
            print(filtered_df.to_string(index=False,formattters={"date":lambda x: x.strftime(CSV.FORMAT)}))
            total_income = filtered_df[filtered_df["category"]=="Income"]["amount"].sum()
            total_expense = filtered_df[filtered_df["category"]=="Expense"]["amount"].sum()
            print("\nSummary:")
            print(f"Total Income: ${total_income:.2f}")
            print(f"Total Expense: ${total_expense:.2f}")
            print(f"Net Savings: ${(total_income - total_expense):.2f}")
            return filtered_df


def add():
    CSV.initialize_csv()
    date = Get_date("Enter The date of the Transaction (dd-mm-yyyy) or Enter for Today's date :",allow_defult=True)
    amount = Get_amount()
    category = Get_category()
    description = Get_description()
    CSV.add_entry(date, amount, category, description)


def plot_transactions(df):
    df.set_index("date",inplace=True)
    income_df = (
        df[df["category"]=="Income"]
        .resample("D")
        .sum
        .reindex(df.index,fill_value=0)
    )
    expense_df = (
        df[df["category"]=="Expense"]
        .resample("D")
        .sum
        .reindex(df.index,fill_value=0)
    )
    plt.figure(figsize=(10,5))
    plt.plot(income_df.index, income_df["amount"],label="Income",color="green")
    plt.plot(expense_df.index, expense_df["amount"],label="Expense",color="red")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expense Over Time")
    plt.legend()
    plt.grid(True)
    plt.show()


def main():
    while True:
        print("\n1. Add a new transaction")
        print("2.View transactions and summary within a date range")
        print("3. Exit")
        choice = input("Enter Your Choice:(1-3) ")

        if choice == "1":
            add()
        elif choice == "2":
            start_date = Get_date("Enter the start date:")
            end_date = Get_date("Enter the end date:")
            df = CSV.get_transactions(start_date,end_date)
            if input("do you want to see a plot ? (y/n) ")=="y":
                plot_transactions(df)
        elif choice == "3":
            print("Exiting!!!.. Thank You")
            break
        else:
            print("Invalid Choice. ENTER 1,2 Or 3,")
if __name__ == "__main__":
    main()


