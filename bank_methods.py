import mysql.connector


def check_balance():
    print("Please select the account that you would like to check.")
    print_accounts()
    return #balance of account selected

def deposit():
    print("Please select the account you would like to deposit into.")
    print_accounts()
    selected_account = input("Enter: ")
    #SQL modify table value
    print("Transaction success!")
    return

def withdrawal():
    print("Please select the account you would like to withdraw from.")
    print_accounts()
    selected_account = input("Enter: ")
    #SQL modify table value
    print("Transaction success!")
    return

def create_account():
    print("Enter Account Name: ")
    if(input("Would you like to add money to this account? ") == "Y"):
        balance_add = input("How much would you like to add? ")
        #sql add new entry into accounts table for user'
    print("Account successfully created. ")
    return

def delete_account():
    print("Please select the account that you would like to delete.")
    print_accounts()
    account = input("Enter: ")
    if(input("Are you certain that you want to delete this account?") == "Y"):
        if(check_balance() > 0):
            print("Please transfer all the funds from your account to another one.")
            transfer_all(account)
    return

def transfer():
    print("Please select the account you would like to transfer funds from. ")
    print_accounts()
    selected_account = input("Enter: ")
    print("Please select the account you would like to transfer funds to.")
    print_accounts(selected_account)
    recipient = input("Enter: ")
    return

def transfer_all(account=""):
    print("Please select the account you would like to transfer your funds to.")
    print_accounts()
    receiving_account = input("Enter: ")
    return

def print_accounts():
    #Select all accounts associated with user and print then out sorted alphabetically
    return

def print_accounts(account=""):
    #print without showing the selected account
    return

def modify_account():
    #Modify values in SQL table.
    return