import time
import json
import os
import math
from datetime import date
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, "data.json")
with open(file_path, "r") as file:
    data = json.load(file)
users = data["users"]
attempt=0
logged_in=False
loggedin_user=None
while True:
    username=input("Enter the username: ")
    password=input("Enter the password: ")
    for user in users.values():
        if username==user["username"] and password==user["password"]:
            logged_in=True
            attempt=0
            loggedin_user=user
            break
    if logged_in:
        break
    attempt+=1
    print(f"Incorrect username or password. Attempt: {attempt}/6")
    if attempt==3:
        for i in range(60,-1,-1):
            print(f"\rPlease wait:{i//60:02d}:{i%60:02d}", end="")
            time.sleep(1)
        print()
        print("You may try again.")
    if attempt==6:
        print("Maximum login attempts exceeded.")
        print("Your card has been blocked.")
        print("Please contact the bank administrator.")

        admin=input("Administrator username: ")
        adminpassword=input("Administrator password: ")
        admin_found=False
        for user in users:
            if user["username"] == admin and user["password"] == adminpassword and user["username"] == "admin":
                admin_found=True
                break
        if admin_found:
            attempt=0
            print("Account has been reset.")
        else:
            break
if logged_in:
    print("=" * 36)
    print(" PYTHON BANKING SYSTEM")
    print("=" * 36)
    print(f"Welcome, {username}!")
    print()
    print("1. View Account Information")
    print("2. Check Balance")
    print("3. Deposit Money")
    print("4. Withdraw Money")
    print("5. Transfer Money")
    print("6. Transaction History")
    print("7. Daily Limits")
    print("8. Change Password")
    print("9. Logout")
    print("0. Exit")
    print("=" * 36)
    choice = input("Enter your choice (0-9): ")
    if choice==3:  

        import math
        from datetime import date

        ATM = 500000            # money in ATM
        USER_1 = 0              # balance with coin
        DAILY_LIMIT = 200000    
        deposit_limit = DAILY_LIMIT   # todays limit
        last_day = date.today()       # this a thing that remain the limit for daily

        # JSON hook (added) 
        from storage import load_state, save_operation
        state = load_state(current_user)      # current_user comes from the login code
        ATM = state["atm"]
        USER_1 = state["balance"]
        deposit_limit -= state["deposit_used"]
        #  end JSON hook 



        def reset_limit_if_new_day():
            global deposit_limit, last_day
            today = date.today()
            if today != last_day:
                last_day = today
                deposit_limit = DAILY_LIMIT
                print("A new day has started. Your daily deposit limit has been reset.")


        def deposit(amount_azn):
            global deposit_limit, ATM, USER_1
            reset_limit_if_new_day()
            k = amount_azn * 100

            if k > deposit_limit:
                print("Sorry, you have exceeded the deposit limit.")
                return False

            deposit_limit -= k
            ATM += k
            USER_1 += k
            return True


        print("The daily min limit for deposit is 1 AZN.")
        print("The daily max limit for deposit is 2,000 AZN.")

        for i in range(100):
            reset_limit_if_new_day()
            print("Remaining deposit limit today =", deposit_limit / 100, "AZN")

            text = input("Enter the amount you wish to deposit: ")

            # checking if the number is a normal number
            try:
                amount = float(text)
                if not math.isfinite(amount):
                    raise ValueError
            except ValueError:
                print("Please enter a valid number.")
                continue

            if int(amount*100) != amount*100:
                print("Please enter a valid number.")
                continue

            if amount < 1:
                print("The minimum deposit is 1 AZN.")
                continue

            balance_before = USER_1   # JSON hook
            if deposit(amount):
                print(amount, "AZN has been transferred to your account.")
                save_operation(current_user, "Deposit", int(round(amount * 100)), 0,   # JSON hook
                            balance_before, USER_1, ATM, "deposit", DAILY_LIMIT - deposit_limit)

            print("Account balance =", USER_1 / 100, "AZN")
    if choice == 4:


        import math
        from datetime import date 
        draw_limit=100000 #qepiynen hesablanır
        commission_limit=50000
        comission=25
        ATM=500000 #kodlar birleşende silenecek 
        USER_1=2000 #meselen yeni buda silinecek
        last_reset_date=date.today() 

        # ---- JSON hook (added) ----
        from storage import load_state, save_operation
        state = load_state(current_user)      # current_user comes from the login code
        ATM = state["atm"]
        USER_1 = state["balance"]
        DRAW_MAX = 100000
        draw_limit -= state["withdraw_used"]
        commission_limit = max(0, commission_limit - state["withdraw_used"])
        # ---- end JSON hook ----

        def reset_limits(): 
            global draw_limit, commission_limit, last_reset_date
            if date.today() != last_reset_date:
                draw_limit=100000
                commission_limit=50000
                last_reset_date=date.today()

        def draw(draw_amount):
            global ATM, USER_1, commission_limit, commission,draw_limit
            reset_limits() #YENİ
            x = draw_amount*100
            if x > draw_limit:
                    print("Sorry, you have exceeded the draw limit.")
                    return False
                
            if x>USER_1:
                print("You do not have a sufficient balance.")
                return False
            p=commission_limit-x
            commission_limit-=x
            if p>=0:
                print("comission is 0 ")
                p=0
            else:
                print("comission is",abs(p)*0.02)
                commission_limit=0
            ATM-=x+p
            USER_1-=x+p
            draw_limit-=x
            return True
        print("The daily min limit for deposit is 1 AZN.")
        print("The daily max limit for deposit is 1000 AZN.")
        print("Account balance =", USER_1 / 100, "AZN")
        print("Remaining draw limit =", draw_limit / 100, "AZN") 
        for i in range(100):
            text = input("Enter the amount you wish to draw: ")

            # checking if the number is a normal number
            try:
                amount = float(text)
                if not math.isfinite(amount):
                    raise ValueError
            except ValueError:
                print("Please enter a valid number.")
                continue
            
            if int(amount*100) != amount*100:
                print("Please enter a valid number.")
                continue

            
            if amount < 1:
                print("The minimum draw is 1 AZN.")
                continue

            balance_before = USER_1   # JSON hook
            if draw(amount):
                print(amount, "AZN has been withdrawn from your account.")
                cash = int(round(amount * 100))   # JSON hook
                save_operation(current_user, "Withdrawal", cash, balance_before - USER_1 - cash,   # JSON hook
                            balance_before, USER_1, ATM, "withdraw", DRAW_MAX - draw_limit)

            print("Account balance =", USER_1 / 100, "AZN")
            print("Remaining draw limit =", draw_limit / 100, "AZN") 
    if choice == "8":
        while True:
            new_password=input("Enter the new password(At least 8 characters and at least 1 uppercase, 1 lowercase, 1 digit): ")
            password_repeat=input("Enter the new password again: ")
            if new_password!=loggedin_user["password"] and new_password==password_repeat:
                if len(new_password)>=8:
                    digit=0
                    upper=0
                    lower=0
                    for i in new_password:
                        if i.isdigit():
                            digit+=1
                        elif i.isupper():
                            upper+=1
                        elif i.islower():
                            lower+=1
                    if upper!=0 and lower!=0 and digit!=0:
                        loggedin_user["password"]=new_password
                        break
                    elif upper==0:
                        print("Weak password: no uppercase letters")
                    elif lower==0:
                        print("Weak password: no lowercase letters")
                    elif digit==0:
                        print("Weak password: no digits")
                else:
                    print("Password have to be at least 8 characters")
            else:
                print("Enter the new password again correctly")
        with open("users.json", "w") as file:
            json.dump(data, file, indent=4)
