if choice==3:  

    import math
    from datetime import date

    ATM = 500000            # money in ATM
    USER_1 = 0              # balance
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




if choice == 4 


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