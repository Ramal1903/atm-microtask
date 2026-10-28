import time
username_1="Kelem"
username_2="Besiktas"
username_3="Baklava"
password_1="Ramal123"
password_2="Eagle1903"
password_3="Nuwolsun123"
balance_1=2500.00
balance_2=1500.00
balance_3=3000.00
attempt=0
admin_username="admin"
admin_password="admin123"
while True:
    username=input("Enter the username: ")
    password=input("Enter the password: ")
    if username==username_1 and password==password_1:
        user=1
        attempt=0
        break
    elif username==username_2 and password==password_2:
        user=2
        attempt=0
        break
    elif username==username_3 and password==password_3:
        user=3
        attempt=0
        break
    else:
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
        if admin==admin_username and adminpassword==admin_password:
            attempt=0
            print("Account has been reseted.")
        else:
            break
