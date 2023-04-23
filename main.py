import mysql.connector
import bank_methods
from datetime import datetime
import tkinter as tk
import random

root = tk.Tk()
works_num = 1

#Establishes connection to the MySQL server
mydb = mysql.connector.connect(
host="localhost",
user="root",
password="7865"
)
mycursor = mydb.cursor()

def get_date():
    current_date = datetime.now()
    date = current_date.strftime("%Y-%m-%d")
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
    for row in rows:
        print(row)
    if(not rows):
        return False
    return True

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

def login(user, password):
    global mycursor
    if(check_username(user)):
        print("Username found")
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute(f"SELECT * FROM example.userbase WHERE Username = '{user}' AND Password = '{password}';")
    row = mycursor.fetchall()
    if(row):
        print("Login success")
    return

def create_new_user(name, user, password, pin):
    global mycursor
    sql = "INSERT INTO `example`.`userbase` (`User_ID`, `Name`, `Username`, `Password`, `Pin`, `Account_Date_Created`) VALUES ('%s', '%s', '%s', '%s', '%s', '%s');"
    generate_id = random.randrange(1, 99999)
    condition = check_user_id(generate_id)
    while(condition):
        print(generate_id)
        generate_id = random.randrange(1, 99999)
        condition = check_user_id(generate_id)
    if(check_empty(name) or check_empty(user) or check_empty(password) or not check_int(pin)):
        return
    val = (generate_id, name, user, password, pin, get_date())
    sql = sql % val
    mycursor.execute(sql)
    print("Success!")
    #mycursor.execute(f"DELETE FROM `example`.`userbase` WHERE (`User_ID` = '{generate_id}');")
    #print("Deleted!")
    mydb.commit()
    return

def clear_page():
    global root
    for widget in root.winfo_children():
        widget.destroy()
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
    title = tk.Label(root, text = "Hello Bank!", font = ('Calibri', 18))
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
    #Creates "Create new user" button
    create_user = tk.Button(root, text = "Create New User", command = lambda : create_user_page())
    create_user.grid(row = main_row + 1, column = main_col, columnspan = 2, padx = 100, pady = 85, sticky = tk.EW + tk.N)
    #https://stackoverflow.com/questions/6920302/how-to-pass-arguments-to-a-button-command-in-tkinter
    #https://www.youtube.com/watch?v=yuuDJ3-EdNQ Creating Buttons With TKinter - Codemy.com
    #Creates login button
    login_button = tk.Button(root, text = "Login", command = lambda : login(username.get(), password.get()))
    login_button.grid(row = main_row + 1, column = main_col, columnspan = 2, padx = 100, pady = 50, sticky = tk.EW + tk.N)
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
                            command = lambda : create_new_user(name.get(), username.get(), password.get(), pin.get()))
    create_user.grid(row = main_row + 1, column = main_col, columnspan = 2, padx = 100, pady = 50, sticky = tk.EW + tk.N)
    #Creates back button
    back_button = tk.Button(root, text = "Back", command = lambda : main_page())
    back_button.grid(row = main_row + 1, column = main_col, columnspan = 2, padx = 100, pady = 75, sticky = tk.EW + tk.N)

    return

def main():
    # print("Create new user.")
    # add new entry into SQL
    # username = input("User: ")
    # password = input("Password: ")
    # if(username == "user"):
    #     if(password == "pass"):
    #         print("Login success.")
    # create_account()
    # bank_methods.delete_account()
    # bank_methods.transfer()
    # bank_methods.deposit()
    # bank_methods.withdrawal()

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

    #Runs GUI object
    root.mainloop()

if __name__=="__main__":
    main()