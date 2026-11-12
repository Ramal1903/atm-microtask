if choice==3:  

    import math
    from datetime import date

    ATM = 500000            # money in ATM
    USER_1 = 0              # balance
    DAILY_LIMIT = 200000    
    deposit_limit = DAILY_LIMIT   # todays limit
    last_day = date.today()       # this a thing that remain the limit for daily



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

        if deposit(amount):
            print(amount, "AZN has been transferred to your account.")

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
    print("Remaining draw limit =", draw_limit / 100, "AZN") #YENİ
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

        if draw(amount):
            print(amount, "AZN has been withdrawn from your account.")

        print("Account balance =", USER_1 / 100, "AZN")
        print("Remaining draw limit =", draw_limit / 100, "AZN") 