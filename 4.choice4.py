# if choice == 4 bunları ramal sen hell ele ayrı ayrı fayl şekilde yazdım birleşdirende choice seçgilerine görə hell edersen


import math
draw_limit=100000 #qepiynen hesablanır
commission_limit=50000
comission=25
ATM=500000 #kodlar birleşende silenecek 
USER_1=2000 #meselen yeni buda silinecek

def draw(draw_amount):
    global ATM, USER_1, commission_limit, commission,draw_limit
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