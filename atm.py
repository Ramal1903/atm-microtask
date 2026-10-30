import time
import json
with open("users.json", "r") as file:
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

