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
    for user in users:
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
    current_user = loggedin_user
    while True:
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
        if choice == "1":
            from storage import load_state

            state = load_state(current_user)

            print("\n=========== ACCOUNT INFORMATION ===========")
            print(f"Account Holder: {current_user['username']}")
            print(f"Account Number: {current_user['ID']}")
            print(f"Available Balance: {state['balance'] / 100:.2f} AZN")
            print(f"Account Status: {current_user.get('status', 'Active')}")
            print("===========================================")
        elif choice == "2":
            from storage import load_state   # JSON hook
            state = load_state(current_user)
            print("Available Balance:", f"{state['balance'] / 100:.2f}", "AZN")
        elif choice == "3":

            import math
            from datetime import date

        
            DAILY_LIMIT = 200000    
            deposit_limit = DAILY_LIMIT   # todays limit
            last_day = date.today()       # this a thing that remain the limit for daily

            # ---- JSON hook (added) ----
            from storage import load_state, save_operation
            state = load_state(current_user)      # current_user comes from the login code
            ATM = state["atm"]
            USER_1 = state["balance"]
            deposit_limit -= state["deposit_used"]
            # ---- end JSON hook ----



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
                k = round(amount_azn * 100)

                if k > deposit_limit:
                    print("Sorry, you have exceeded the deposit limit.")
                    return False

                deposit_limit -= k
                ATM += k
                USER_1 += k
                return True


            print("Deposits must be positive, with at most 2 decimal places.")
            print("The daily max limit for deposit is 2,000 AZN.")

            for i in range(100):
                reset_limit_if_new_day()
                print("Remaining deposit limit today =", f"{deposit_limit / 100:.2f}", "AZN")

                text = input("Enter the amount you wish to deposit (0 = back to menu): ")
                if text.strip() == "0":
                    break

                # checking if the number is a normal number
                try:
                    amount = float(text)
                    if not math.isfinite(amount):
                        raise ValueError
                except ValueError:
                    print("Please enter a valid amount (positive number, at most 2 decimal places).")
                    continue

                if abs(round(amount*100) - amount*100) > 1e-6:
                    print("Please enter a valid amount (positive number, at most 2 decimal places).")
                    continue

                if amount <= 0:
                    print("The amount must be greater than 0.")
                    continue

                balance_before = USER_1   # JSON hook
                if deposit(amount):
                    print(f"{amount:.2f}", "AZN has been transferred to your account.")
                    save_operation(current_user, "Deposit", int(round(amount * 100)), 0,   # JSON hook
                                balance_before, USER_1, ATM, "deposit", DAILY_LIMIT - deposit_limit)

                print("Account balance =", f"{USER_1 / 100:.2f}", "AZN")




        elif choice == "4": 


            import math
            from datetime import date 
            draw_limit=100000 #qepiynen hesablanır
            commission_limit=50000
            last_reset_date=date.today() 

            # JSON hook 
            from storage import load_state, save_operation
            state = load_state(current_user)      # current_user comes from the login code
            ATM = state["atm"]
            USER_1 = state["balance"]
            DRAW_MAX = 100000
            draw_limit -= state["withdraw_used"]
            commission_limit = max(0, commission_limit - state["withdraw_used"])
            #  end JSON hook 

            def reset_limits(): 
                global draw_limit, commission_limit, last_reset_date
                if date.today() != last_reset_date:
                    draw_limit=100000
                    commission_limit=50000
                    last_reset_date=date.today()

            def draw(draw_amount):
                global ATM, USER_1, commission_limit,draw_limit
                reset_limits() 
                x = round(draw_amount*100)
                if x > draw_limit:
                        print("Sorry, you have exceeded the draw limit.")
                        return False
                    
                p=commission_limit-x
                fee = 0 if p>=0 else (abs(p)*2 + 50)//100   # 2% 
                if x+fee>USER_1:
                    print("You do not have a sufficient balance.")
                    return False
                if x>ATM:
                    print("Transaction declined: insufficient ATM cash.")
                    return False
                commission_limit-=x
                if p>=0:
                    print("comission is 0.00 AZN")
                else:
                    print("comission is", f"{fee/100:.2f}", "AZN")
                    commission_limit=0
                ATM-=x
                USER_1-=x+fee
                draw_limit-=x
                return True
            print("Fee-free withdrawals: 500 AZN per day (2% fee on the excess).")
            print("The daily max limit for withdrawal is 1000 AZN.")
            print("Account balance =", f"{USER_1 / 100:.2f}", "AZN")
            print("Remaining draw limit =", f"{draw_limit / 100:.2f}", "AZN") 
            for i in range(100):
                text = input("Enter the amount you wish to draw (0 = back to menu): ")
                if text.strip() == "0":
                    break

                # checking if the number is a normal number
                try:
                    amount = float(text)
                    if not math.isfinite(amount):
                        raise ValueError
                except ValueError:
                    print("Please enter a valid amount (positive number, at most 2 decimal places).")
                    continue
                
                if abs(round(amount*100) - amount*100) > 1e-6:
                    print("Please enter a valid amount (positive number, at most 2 decimal places).")
                    continue

                
                if amount <= 0:
                    print("The amount must be greater than 0.")
                    continue

                balance_before = USER_1   # JSON hook
                if draw(amount):
                    print(f"{amount:.2f}", "AZN has been withdrawn from your account.")
                    cash = int(round(amount * 100))   # JSON hook
                    save_operation(current_user, "Withdrawal", cash, balance_before - USER_1 - cash,   # JSON hook
                                balance_before, USER_1, ATM, "withdraw", DRAW_MAX - draw_limit)

                print("Account balance =", f"{USER_1 / 100:.2f}", "AZN")
                print("Remaining draw limit =", f"{draw_limit / 100:.2f}", "AZN") 
        elif choice == "5":
            import datetime
            from datetime import date
            from storage import load_transfer_state, save_transfer_state

            transfer_limit1 = 5  

            print("\n--- TRANSFER BETWEEN USERS ---")
            recipient_acc = input("Enter the recipient's account number: ")

            
            t = load_transfer_state(current_user, recipient_acc)
            acc1_no = t["acc1_no"]
            balance1 = t["balance1"] / 100
            outgoing_transfers1 = t["outgoing_transfers1"]
            history1 = t["history1"]
            acc2_no = t["acc2_no"]
            balance2 = t["balance2"] / 100
            history2 = t["history2"]
           

            if recipient_acc == acc2_no:
                transfer_amount = float(input("Enter the amount to transfer (AZN): "))

                if transfer_amount > 0 and transfer_amount <= balance1 and outgoing_transfers1 < transfer_limit1:
                    print(f"Sender: {t['username1']}")
                    print(f"Recipient account: {recipient_acc}")
                    print(f"Recipient: {t['username2']}")
                    print(f"Amount: {transfer_amount:.2f} AZN")
                    confirm = input("Confirm transfer (Y/N): ").strip().upper()

                    if confirm == 'Y':
                        # Göndərənin məlumatları.
                        b_before_sender = balance1
                        balance1 -= transfer_amount
                        b_after_sender = balance1
                        outgoing_transfers1 += 1

                        txn_id_s = f"TXN000{len(history1) + 1}"
                        txn_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                        history1.append({
                            "id": txn_id_s,
                            "date": txn_date,
                            "type": "Transfer Sent",
                            "amount": -transfer_amount,
                            "before": b_before_sender,
                            "after": b_after_sender,
                            "recipient": recipient_acc
                        })

                        # Alıcının məlumatları
                        b_before_rec = balance2
                        balance2 += transfer_amount
                        b_after_rec = balance2

                        txn_id_r = f"TXN000{len(history2) + 1}"
                        history2.append({
                            "id": txn_id_r,
                            "date": txn_date,
                            "type": "Transfer Received",
                            "amount": transfer_amount,
                            "before": b_before_rec,
                            "after": b_after_rec,
                            "recipient": acc1_no
                        })
        
        elif choice == "6":
            from storage import load_history

            history1 = load_history(current_user)

            print("\n--- TRANSACTION HISTORY ---")
            print(f"History of {current_user['username']}:")
            if not history1:
                print("No transactions yet.")
            for i, txn in enumerate(history1, start=1):
                amount = txn['amount']
                if txn['type'] in ("Withdrawal", "Transfer Sent"):
                    amount = -amount
                print(f"ID: {txn.get('id', f'TXN000{i}')}")
                print(f"Date: {txn['date']}")
                print(f"Type: {txn['type']}")
                print(f"Amount: {amount:.2f} AZN")
                print(f"Balance before: {txn['balance_before']:.2f} AZN")
                print(f"Balance after: {txn['balance_after']:.2f} AZN")
                if txn.get('recipient', "N/A") != "N/A":
                    print(f"Recipient account: {txn['recipient']}")
                print("-" * 30)
        elif choice == "7":
                from storage import load_state
        
                state = load_state(current_user)
        
                deposit_limit1 = 2000.00          # daily deposit limit (AZN)
                cash_limit1 = 1000.00             # daily withdrawal limit (AZN)
                transfer_limit1 = 5               # max outgoing transfers per day
        
                deposit_used1 = state["deposit_used"] / 100
                cash_withdrawn1 = state["withdraw_used"] / 100
                fee_free_limit1 = max(0, 500.00 - cash_withdrawn1)
                outgoing_transfers1 = state["transfers_used"]
        
                print("=========== DAILY LIMITS ===========")
                print(f"Deposit used:          {deposit_used1:.2f} / {deposit_limit1:.2f} AZN")
                print(f"Deposit remaining:     {deposit_limit1 - deposit_used1:.2f} AZN")
                print(f"Cash withdrawn:        {cash_withdrawn1:.2f} / {cash_limit1:.2f} AZN")
                print(f"Cash withdrawal remaining: {cash_limit1 - cash_withdrawn1:.2f} AZN")
                print(f"Fee-free cash remaining: {fee_free_limit1:.2f} AZN")
                print(f"Outgoing transfers:    {outgoing_transfers1} / {transfer_limit1}")
                print("====================================")
        elif choice == "8":
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
                            print("Password changed successfully.")
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
            with open(file_path, "w") as file:
                json.dump(data, file, indent=4)
        elif choice == "9":
            print("Logged out successfully.")
            break
        elif choice == "0":
            print("Thank you for using Python Banking System.")
            break
        else:
            print("Invalid choice. Please try again.")
