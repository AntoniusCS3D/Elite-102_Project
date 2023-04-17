import mysql
import bank_methods

def main():
    print("Create new user.")
    #add new entry into
    username = input("User: ")
    password = input("Password: ")
    if(username == "user"):
        if(password == "pass"):
            print("Login success.")
    # create_account()
    bank_methods.delete_account()
    bank_methods.transfer()
    bank_methods.deposit()
    bank_methods.withdrawal()
main()