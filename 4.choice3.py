# if choice==3:  #ramal bunları sen daxil ele

import math

ATM = 500000            # money in ATM
USER_1 = 0              # balance
deposit_limit = 200000  # the limit üith qepik


def deposit(amount_azn):
    global deposit_limit, ATM, USER_1
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
