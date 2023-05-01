import mysql.connector
from datetime import datetime
import tkinter as tk
from random import randrange

root = tk.Tk()
works_num = 1

#Establishes connection to the MySQL server (Change these details to your connection)
mydb = mysql.connector.connect(
host="localhost",
user="root",
password="7865"
)
mycursor = mydb.cursor()

# user_base = "userbase"
# user_base_columns = ("User_ID", "INT", "PRIMARY KEY", "NOT NULL"), 
# ("Name", "VARCHAR(45)", "NOT NULL"), 
# ("Username", "VARCHAR(45)", "NOT NULL", "UNIQUE"), 
# ("Password", "VARCHAR(45)", "NOT NULL"),
# ("Pin", "INT", "NOT NULL")
# ("Account_date_created", "DATE", "NOT NULL")

def get_date():
    current_date = datetime.now()
    date = current_date.strftime("%Y-%m-%d")
    return date

def get_datetime():
    current_date = datetime.now()
    date = current_date.strftime("%Y-%m-%d %H:%M:%S")
    return date

def check_user_id(user_id):
    #https://stackoverflow.com/questions/38350816/python-mysql-connector-internalerror-unread-result-found-when-close-cursor
    #https://stackoverflow.com/questions/48899190/cannot-create-a-database-due-to-error-mysqlconnection-object-is-not-callable
    #https://stackoverflow.com/questions/10195139/how-to-retrieve-sql-result-column-value-using-column-name-in-python
    #https://www.tutorialspoint.com/how-can-you-test-if-some-record-exists-or-not-in-a-mysql-table-using-python
    global mycursor
    global mydb
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute(f"SELECT * FROM example.userbase WHERE User_ID = {user_id};")
    #tests if function works
    #mycursor.execute(f"SELECT * FROM example.userbase WHERE User_ID = 6479;")
    rows = mycursor.fetchall()
    if(rows):
        return True
    return False

def check_accountnum(user_id):
    global mycursor
    global mydb
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute(f"SELECT * FROM example.userbase WHERE User_ID = {user_id};")
    #tests if function works
    #mycursor.execute(f"SELECT * FROM example.userbase WHERE User_ID = 6479;")
    rows = mycursor.fetchall()
    if(rows):
        return True
    return False

def check_username(username):
    global mycursor
    global mydb
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute(f"SELECT * FROM example.userbase WHERE Username = '{username}';")
    rows = mycursor.fetchone()
    if(rows):
        return True
    return False

def check_empty(string):
    if(str(string) == ''):
        return True
    return False

def check_int(num):
    try: 
        int(num)
    except(ValueError):
        return False
    return True

def clear_page():
    global root
    for widget in root.winfo_children():
        widget.destroy()
    return

def login(user, password):
    #https://stackoverflow.com/questions/5010042/mysql-get-column-name-or-alias-from-query
    global mycursor
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute(f"SELECT * FROM example.userbase WHERE Username = '{user}' AND Password = '{password}';")
    values = mycursor.fetchone()
    if(values):
        field_name = [i[0] for i in mycursor.description]
        row = dict(zip(field_name, values))
        user_page(row['User_ID'])
    return

def withdrawal(user_id, account_number, amount):
    global mycursor
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute(f"SELECT * FROM example.accounts WHERE Account_number = {account_number};")
    account = mycursor.fetchone()
    field_name = [i[0] for i in mycursor.description]
    row = dict(zip(field_name, account))
    account_bal = row['Balance']
    if(float(account_bal) < float(amount)):
        return "invalid"
    new_bal = account_bal - float(amount)
    sql = "INSERT INTO `example`.`transaction_history` (`Account_number`, `Amount`, `Balance`, `Sender`, `Recipient`, `Date_Transaction`) VALUES ('%s', '%s', '%s', '%s', '%s', '%s');"
    val = (account_number, f"-${amount}", new_bal, "Bank", "You", get_datetime())
    sql = sql % val
    mycursor.execute(sql)
    mydb.commit()
    sql = f"UPDATE `example`.`accounts` SET `Balance` = '{new_bal}' WHERE (`Account_number` = '{account_number}');"
    mycursor.execute(sql)
    mydb.commit()
    return

def deposit(user_id, account_number, amount):
    global mycursor
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute(f"SELECT * FROM example.accounts WHERE Account_number = {account_number};")
    account = mycursor.fetchone()
    field_name = [i[0] for i in mycursor.description]
    row = dict(zip(field_name, account))
    account_bal = row['Balance']
    new_bal = account_bal + float(amount)
    sql = "INSERT INTO `example`.`transaction_history` (`Account_number`, `Amount`, `Balance`, `Sender`, `Recipient`, `Date_Transaction`) VALUES ('%s', '%s', '%s', '%s', '%s', '%s');"
    val = (account_number, f"+${amount}", new_bal, "You", "Bank", get_datetime())
    sql = sql % val
    mycursor.execute(sql)
    sql = f"UPDATE `example`.`accounts` SET `Balance` = '{new_bal}' WHERE (`Account_number` = '{account_number}');"
    mycursor.execute(sql)
    mydb.commit()
    return

def create_new_account(user_id, name):
    global mycursor
    sql = "INSERT INTO `example`.`accounts` (`Account_number`, `Routing_number`, `User_ID`, `Account_name`, `Balance`, `Date_created`, `Date_last_accessed`) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s');"
    # https://stackoverflow.com/questions/3505831/in-python-how-do-i-convert-a-single-digit-number-into-a-double-digits-string
    generate_accountnum = f"1{randrange(1, 99):02}{user_id:010}"
    condition = check_accountnum(generate_accountnum)
    while(condition):
        generate_accountnum = randrange(1, 99999)
        condition = check_accountnum(generate_accountnum)
    if(check_empty(name)):
        return
    val = (generate_accountnum, 123456789, user_id, name, 0.0, get_date(), get_date())
    sql = sql % val
    mycursor.execute(sql)
    mydb.commit()
    return

def create_new_user(name, user, password, pin):
    global mycursor
    sql = "INSERT INTO `example`.`userbase` (`User_ID`, `Name`, `Username`, `Password`, `Pin`, `Account_Date_Created`) VALUES ('%s', '%s', '%s', '%s', '%s', '%s');"
    generate_id = randrange(1, 99999)
    condition = check_user_id(generate_id)
    while(condition):
        generate_id = randrange(1, 99999)
        condition = check_user_id(generate_id)
    if(check_empty(name) or check_empty(user) or check_empty(password) or not check_int(pin)):
        return
    val = (generate_id, name, user, password, pin, get_date())
    sql = sql % val
    mycursor.execute(sql)
    mydb.commit()
    return

def create_user_and_back(name, user, password, pin):
    create_account_and_back(name, user, password, pin)
    main_page()

def withdrawal_and_back(user_id, account_num, amount):
    if(withdrawal(user_id, account_num, amount) == "invalid"):
        return
    transactionhistory_page(user_id, account_num)

def deposit_and_back(user_id, account_num, amount):
    deposit(user_id, account_num, amount)
    transactionhistory_page(user_id, account_num)

def create_account_and_back(user_id, name):
    create_new_account(user_id, name)
    user_page(user_id)
    return

def withdrawal_page(user_id, account_number):
    clear_page()
    #Changes in position of title will affect everything else
    #Modify main_row and main_col to change row and col of all elements
    main_row = 1
    main_col = 1
    #Creates title label
    title = tk.Label(root, text = "Withdrawal", font = ('Calibri', 18))
    title.grid(row = main_row - 1, column = main_col, columnspan = 2, pady = 25, sticky = tk.S)
    #Creates withdraw label
    withdraw_label = tk.Label(root, text = "Amount: ")
    withdraw_label.grid(row = main_row, column = main_col, sticky = tk.E)
    #Creates withdraw entry box
    amount = tk.StringVar()
    withdraw_entry = tk.Entry(root, textvariable = amount)
    withdraw_entry.grid(row = main_row, column = main_col + 1, sticky = tk.W)
    #Creates withdraw button
    withdraw_button = tk.Button(root, text = "Withdraw", command = lambda : withdrawal_and_back(user_id, account_number, amount.get()))
    withdraw_button.grid(row = main_row + 1, column = main_col, columnspan = 2, pady = 55, sticky = tk.EW + tk.N)
    #Creates back button
    back_button = tk.Button(root, text = "Back", command = lambda : transactionhistory_page(user_id, account_number))
    back_button.grid(row = main_row + 1, column = main_col, columnspan = 2, pady = 75, sticky = tk.EW + tk.N)
    return

def deposit_page(user_id, account_number):
    clear_page()
    #Changes in position of title will affect everything else
    #Modify main_row and main_col to change row and col of all elements
    main_row = 1
    main_col = 1
    #Creates title label
    title = tk.Label(root, text = "Deposit", font = ('Calibri', 18))
    title.grid(row = main_row - 1, column = main_col, columnspan = 2, pady = 25, sticky = tk.S)
    #Creates deposit label
    deposit_label = tk.Label(root, text = "Amount: ")
    deposit_label.grid(row = main_row, column = main_col, sticky = tk.E)
    #Creates deposit entry box
    amount = tk.StringVar()
    deposit_entry = tk.Entry(root, textvariable = amount)
    deposit_entry.grid(row = main_row, column = main_col + 1, sticky = tk.W)
    #Creates withdraw button
    deposit_button = tk.Button(root, text = "Deposit", command = lambda : deposit_and_back(user_id, account_number, amount.get()))
    deposit_button.grid(row = main_row + 1, column = main_col, columnspan = 2, pady = 55, sticky = tk.EW + tk.N)
    #Creates back button
    back_button = tk.Button(root, text = "Back", command = lambda : transactionhistory_page(user_id, account_number))
    back_button.grid(row = main_row + 1, column = main_col, columnspan = 2, pady = 75, sticky = tk.EW + tk.N)
    return

def user_page(user_id):
    clear_page()
    for i in range(4):
        root.grid_columnconfigure(i, weight = 1)
    for i in range(5):
        root.grid_rowconfigure(i, weight = 1)
    #Changes in position of title will affect everything else
    #Modify main_row and main_col to change row and col of all elements
    main_row = 1
    main_col = 1
    #Search for accounts
    global mycursor
    global mydb
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute(f"SELECT * FROM example.accounts WHERE User_ID = {user_id};")
    rows = mycursor.fetchall()
    #Create click/hover frames that show account name and balance
    if(not (rows == None)):
        iter = 0
        account_frame = tk.Frame(root, bg = "white", height = 2)
        account_frame.grid(row = 0, rowspan = 1, column = main_col, columnspan = 3, sticky = tk.EW)
        account_frame.grid_columnconfigure(0, weight = 1)
        account_frame.grid_columnconfigure(1, weight = 2)
        for num in rows:
            field_name = [i[0] for i in mycursor.description]
            account = dict(zip(field_name, num))
            account_name = account['Account_name']
            balance = account['Balance']
            account_num = account['Account_number']
            account_label = tk.Label(account_frame, text = f"{account_name}", bg = "white", height = 2)
            account_label.grid(row = iter, column = 0, sticky = tk.EW)
            balance_button = tk.Button(account_frame, text = f"${balance}", bg = "white", height = 2, width = 5, command = lambda account_num = account_num: transactionhistory_page(user_id, account_num))
            balance_button.grid(row = iter, column = 1, sticky = tk.EW)
            iter = iter + 1
    #Create new createaccount button
    createaccount_button = tk.Button(root, text = "Create account", command = lambda : newaccount_page(user_id))
    createaccount_button.grid(row = main_row + 1, column = main_col, columnspan = 2, padx = 100, pady = 50, sticky = tk.EW + tk.N)
    #Creates logout button
    logout_button = tk.Button(root, text = "Logout", command = lambda : main_page())
    logout_button.grid(row = main_row + 1, column = main_col, columnspan = 2, padx = 100, pady = 75, sticky = tk.EW + tk.N)
    return

def transactionhistory_page(user_id, account_num):
    clear_page()
    for i in range(4):
        root.grid_columnconfigure(i, weight = 1)
    for i in range(5):
        root.grid_rowconfigure(i, weight = 1)
    #Changes in position of title will affect everything else
    #Modify main_row and main_col to change row and col of all elements
    main_row = 1
    main_col = 1
    #Search for accounts
    global mycursor
    global mydb
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute(f"SELECT * FROM example.transaction_history WHERE Account_number = {account_num};")
    rows = mycursor.fetchall()
    transaction = []
    #Create click/hover frames that show account name and balance
    if(rows):
        iter = 0
        frame = tk.Frame(root, bg = "white", height = 2)
        frame.grid(row = 0, rowspan = 1, column = main_col, columnspan = 3, sticky = tk.EW)
        frame.grid_columnconfigure(0, weight = 1)
        frame.grid_columnconfigure(1, weight = 2)
        for num in rows:
            field_name = [i[0] for i in mycursor.description]
            transaction = dict(zip(field_name, num))
            date = transaction['Date_Transaction']
            account_label = tk.Label(frame, text = f"{date}", bg = "white", height = 2)
            account_label.grid(row = iter, column = 0, sticky = tk.W)
            amount = transaction['Amount']
            amount_label = tk.Label(frame, text = f"Amount: {amount}", bg = "white", height = 2)
            amount_label.grid(row = iter, column = 1, sticky = tk.E)
            iter = iter + 1
    else:
        empty_label = tk.Label(root, text = "No transaction found!", bg = "white")
        empty_label.grid(row = main_row, column = main_col, columnspan = 2, sticky = tk.EW)
    #Show balance
    balance_label = tk.Label(root, text = f"Balance: ${transaction['Balance']}", bg = "white")
    balance_label.grid(row = main_row + 1, column = main_col, columnspan = 2, sticky = tk.EW + tk.N)
    #Create new withdraw button
    withdraw_button = tk.Button(root, text = "Withdraw", command = lambda : withdrawal_page(user_id, account_num))
    withdraw_button.grid(row = main_row + 1, column = main_col, columnspan = 2, padx = 100, pady = 35, sticky = tk.EW + tk.N)
    #Create new deposit button
    deposit_button = tk.Button(root, text = "Deposit", command = lambda : deposit_page(user_id, account_num))
    deposit_button.grid(row = main_row + 1, column = main_col, columnspan = 2, padx = 100, pady = 55, sticky = tk.EW + tk.N)
    #Creates back button
    back_button = tk.Button(root, text = "Back", command = lambda : user_page(user_id))
    back_button.grid(row = main_row + 1, column = main_col, columnspan = 2, padx = 100, pady = 75, sticky = tk.EW + tk.N)
    return

def newaccount_page(user_id):
    clear_page()

    for i in range(4):
        root.grid_columnconfigure(i, weight = 1)
    for i in range(5):
        root.grid_rowconfigure(i, weight = 1)

    #Changes in position of title will affect everything else
    #Modify main_row and main_col to change row and col of all elements
    main_row = 1
    main_col = 1
    #Creates title label
    title = tk.Label(root, text = "New Account", font = ('Calibri', 18))
    title.grid(row=main_row, column = main_col, columnspan = 2, pady = 45, sticky = tk.EW + tk.S)
    #Creates name label
    name_label = tk.Label(root, text = "Account Name: ")
    name_label.grid(row = main_row, column = main_col, pady = 20, sticky = tk.E + tk.S) 
    #Creates name entry box
    name = tk.StringVar()
    name_entry = tk.Entry(root, textvariable=name)
    name_entry.grid(row = main_row, column = main_col + 1, pady = 20, sticky = tk.W + tk.S)
    #Creates "Create new account" button
    create_account = tk.Button(root, text = "Create Account", command = lambda : create_account_and_back(user_id, name.get()))
    create_account.grid(row = main_row + 1, column = main_col, columnspan = 2, padx = 100, pady = 55, sticky = tk.EW + tk.N)
    #Creates back button
    back_button = tk.Button(root, text = "Back", command = lambda : user_page(user_id))
    back_button.grid(row = main_row + 1, column = main_col, columnspan = 2, padx = 100, pady = 75, sticky = tk.EW + tk.N)
    return

def create_user_page():
    clear_page()
    for i in range(4):
        root.grid_columnconfigure(i, weight = 1)
    for i in range(5):
        root.grid_rowconfigure(i, weight = 1)
    
    #Changes in position of title will affect everything else
    #Modify main_row and main_col to change row and col of all elements
    main_row = 1
    main_col = 1

    #Creates title label
    title = tk.Label(root, text = "New User", font = ('Calibri', 18))
    title.grid(row=main_row, column = main_col, columnspan = 2, pady = 45, sticky = tk.EW + tk.S)
    #Creates name label
    name_label = tk.Label(root, text = "Full Legal Name: ")
    name_label.grid(row = main_row, column = main_col, pady = 20, sticky = tk.E + tk.S) 
    #Creates name entry box
    name = tk.StringVar()
    name_entry = tk.Entry(root, textvariable=name)
    name_entry.grid(row = main_row, column = main_col + 1, pady = 20, sticky = tk.W + tk.S)
    #Creates username label
    user_label = tk.Label(root, text = "New Username: ")
    user_label.grid(row = main_row, column = main_col, sticky = tk.E + tk.S) 
    #Creates username entry box
    username = tk.StringVar()
    user_entry = tk.Entry(root, textvariable=username)
    user_entry.grid(row = main_row, column = main_col + 1, sticky = tk.W + tk.S)
    #Creates password label
    password_label = tk.Label(root, text = "New Password: ")
    password_label.grid(row = main_row + 1, column = main_col, sticky = tk.E + tk.N)
    #Creates password entry box
    password = tk.StringVar()
    pass_entry = tk.Entry(root, textvariable = password, show = "*")
    pass_entry.grid(row = main_row + 1, column = main_col + 1, sticky = tk.W + tk.N)
    #Creates pin label
    pin_label = tk.Label(root, text = "New PIN: ")
    pin_label.grid(row = main_row + 1, column = main_col, pady = 20, sticky = tk.E + tk.N)
    #Creates pin entry box
    pin = tk.StringVar()
    pin_entry = tk.Entry(root, textvariable = pin, show = "*")
    pin_entry.grid(row = main_row + 1, column = main_col + 1, pady = 20, sticky = tk.W + tk.N)
    #Creates "Create new user" button
    create_user = tk.Button(root, text = "Create User", 
                            command = lambda : create_user_and_back(name.get(), username.get(), password.get(), pin.get()))
    create_user.grid(row = main_row + 1, column = main_col, columnspan = 2, padx = 100, pady = 55, sticky = tk.EW + tk.N)
    #Creates back button
    back_button = tk.Button(root, text = "Back", command = lambda : main_page())
    back_button.grid(row = main_row + 1, column = main_col, columnspan = 2, padx = 100, pady = 75, sticky = tk.EW + tk.N)
    return

def main_page():
    clear_page()
    #https://www.pythontutorial.net/tkinter/tkinter-grid/
    #root.grid_rowconfigure(0, weight=1)
    for i in range(4):
        root.grid_columnconfigure(i, weight = 1)
    for i in range(5):
        root.grid_rowconfigure(i, weight = 1)

    #Changes in position of title will affect everything else
    #Modify main_row and main_col to change row and col of all elements
    main_row = 1
    main_col = 1

    #Creates title label
    title = tk.Label(root, text = "BANK", font = ('Calibri', 18))
    title.grid(row=main_row, column = main_col, columnspan = 2, pady = 25, sticky = tk.EW + tk.S)
    #Creates username label
    user_label = tk.Label(root, text = "Username: ")
    user_label.grid(row = main_row, column = main_col, sticky = tk.E + tk.S) 
    #Creates username entry box
    username = tk.StringVar()
    user_entry = tk.Entry(root, textvariable=username)
    user_entry.grid(row = main_row, column = main_col + 1, sticky = tk.W + tk.S)
    #Creates password label
    password_label = tk.Label(root, text = "Password: ")
    password_label.grid(row = main_row + 1, column = main_col, sticky = tk.E + tk.N)
    #Creates password entry box
    password = tk.StringVar()
    pass_entry = tk.Entry(root, textvariable = password, show = "*")
    pass_entry.grid(row = main_row + 1, column = main_col + 1, sticky = tk.W + tk.N)
    #https://stackoverflow.com/questions/6920302/how-to-pass-arguments-to-a-button-command-in-tkinter
    #https://www.youtube.com/watch?v=yuuDJ3-EdNQ Creating Buttons With TKinter - Codemy.com
    #Creates login button
    login_button = tk.Button(root, text = "Login", command = lambda : login(username.get(), password.get()))
    login_button.grid(row = main_row + 1, column = main_col, columnspan = 2, padx = 100, pady = 50, sticky = tk.EW + tk.N)
    #Creates "Create new user" button
    create_user = tk.Button(root, text = "Create New User", command = lambda : create_user_page())
    create_user.grid(row = main_row + 1, column = main_col, columnspan = 2, padx = 100, pady = 85, sticky = tk.EW + tk.N)
    return

def main():
    #Basic TKinter GUI fundamental setup
    #https://stackoverflow.com/questions/22421888/tkinter-windows-without-title-bar-but-resizable
    #root.overrideredirect(True)
    #https://stackoverflow.com/questions/3352918/how-to-center-a-window-on-the-screen-in-tkinter
    window_width = 300
    window_height = 400
    get_screen_width = root.winfo_screenwidth()
    get_screen_height = root.winfo_screenheight()
    x_coord = int((get_screen_width / 2) - (window_width / 2))
    y_coord = int((get_screen_height / 2) - (window_height / 2) - 30)
    root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_coord, y_coord))

    #Creates the home page
    main_page()

    #Runs GUI
    root.mainloop()

if __name__=="__main__":
    main()