from datetime import datetime

date_format='%d-%m-%Y'
CATEGORIES = {"I": "Income", "E": "Expense"}

#Promt Use For Ask a client Like Input for Dates For Differnt Reason
# allow_defult = its use for When Client Hit enter use defult date for it And dont need Date Becuase Date its Today

def Get_date(prompt,allow_defult=False):
    date_str = input(prompt)
    if allow_defult and not date_str:
        return datetime.today().strftime(date_format)
    try:
        valid_date = datetime.strptime(date_str, date_format)
        return valid_date.strftime(date_format)

    except ValueError:
        print("Please enter a valid date")
        print(prompt,allow_defult)

def Get_amount():
    try:
        amount = float(input("Enter the amount:"))
        if amount <= 0:
            raise ValueError("Amount must be positive")
        return amount
    except ValueError as e:
        print(e)
        return Get_amount()

def Get_category():
    category = input("Enter the category('I' for Income Or 'E' For Expense)").upper()
    if category in CATEGORIES:
        return CATEGORIES[category]
    print("Please enter a valid category. Please enter 'I' for Income or 'E' for Expense'")
    return Get_category()
def Get_description():
    return input("Enter the description(optional):").upper()


