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

theUsername = input("Enter your username: ")
thePassword=input("Enter your password: ")
while True:
    if thePassword==loggedin_user["password"] and theUsername==loggedin_user["username"]:
        new_password=input("Enter the new password(At least 8 characters and at least 1 uppercase, 1 lowercase, 1 digit): ")
        password_repeat=input("Enter the new password again: ")
        if new_password==password_repeat:
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