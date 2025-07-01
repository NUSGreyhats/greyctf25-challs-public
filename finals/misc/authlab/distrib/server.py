#!/usr/local/bin/python

import pickle, string, random, time
from Creds import Creds
from sys import exit
from base64 import b64encode, b64decode

class AuthLab:
    def __init__(self):
        self.currUser = None
    
    def loginMenu(self):
        return """\n\n\n
[L] Login
[E] Login with EasyCreds
[G] Proceed as Guest
[S] Signup
[Q] Quit
"""

    def login(self):
        print("\033[4mUser Login\033[0m")

        username = input("Username: ")

        password = input("Password: ")
        if len(password) < 35:
            raise Exception("Password is too short, are you sure it is correct?")
        
        status,output = Creds.login(username, password)
        if (not status):
            raise Exception(output)
        if output.rank == Creds.Rank.ADMIN:
            print("\n(•_•)", flush=True)
            time.sleep(0.8)
            print("( •_•)>⌐■-■", flush=True)
            time.sleep(0.8)
            print("(⌐■_■)", flush=True)
            time.sleep(0.8)
        return output

    def easyLogin(self):
        try:
            user = pickle.loads(b64decode(input("Enter EasyCreds: ")))
            if user.rank == Creds.Rank.USER:
                Creds.storePassword(user)
            elif user.rank == Creds.Rank.ADMIN:
                print("\n(•_•)", flush=True)
                time.sleep(0.8)
                print("( •_•)>⌐■-■", flush=True)
                time.sleep(0.8)
                print("(⌐■_■)", flush=True)
                time.sleep(0.8)
            return user
        except:
            raise Exception("Invalid EasyCreds")

    def signup(self):
        print("\033[4mSignup for service\033[0m")
        
        username = input("Username: ")
        if not Creds.isValidUsername(username):
            raise Exception("Invalid username, choose a different one.")
        
        password = ""
        while True:
            password = input("Generate a random password [Y/N]: ").upper()[0]
            if password == "Y":
                password = "".join(random.choices(string.printable[:94], k=35))
                # print(f'Your password: {password}')
                break
            else:
                password = input("Password: ")
                if len(password) < 35:
                    print("\33[0;31mPassword is too short\33[0m\n")
                    continue
                break
        
        status,output = Creds.signup(username, password)
        if (not status):
            raise Exception(output)
        else:
            return output

    def guest(self):
        return Creds.guest()[1]

    def serviceMenu(self):
        return f'''\n\n\n
Welcome {self.currUser}
[S] Service
[L] Logout
[E] Print EasyCreds'''

    def easyCreds(self):
        return b64encode(pickle.dumps(self.currUser)).decode()

    def logout(self):
        if self.currUser.rank == Creds.Rank.ADMIN:
            print("(⌐■_■)", flush=True)
            time.sleep(0.8)
            print("( •_•)>⌐■-■", flush=True)
            time.sleep(0.8)
            print("(•_•)", flush=True)
            time.sleep(0.8)
        return None

    def authenticate(self, service):
        def wrapper():
            while True:
                if self.currUser == None:    # not logged in
                    print(self.loginMenu())
                    choice = input("> ").upper()[0]
                    print()
                    try:
                        if (choice == 'L'):
                            self.currUser = self.login()
                        elif (choice == 'E'):
                            self.currUser = self.easyLogin()
                        elif (choice == 'G'):
                            self.currUser = self.guest()
                        elif (choice == 'S'):
                            self.currUser = self.signup()
                            print(f'\nYour EasyCreds: {self.easyCreds()}')
                        elif (choice == 'Q'):
                            exit(0)
                    except Exception as e:
                        print(f'\33[0;31m{e}\33[0m')
                else:
                    print(self.serviceMenu())
                    choice = input("> ").upper()[0]
                    print()
                    if (choice == 'S'):
                        try:
                            service(self.currUser)
                        except Exception as e:
                            self.currUser = None
                            print(f'\33[0;31m{e}\33[0m')
                    elif (choice == 'L'):
                        self.currUser = self.logout()
                        print("\nLogged out\n")
                    elif (choice == 'E'):
                        print(f'\nYour EasyCreds: {self.easyCreds()}')
        return wrapper



al = AuthLab()

@al.authenticate
def dummy_service(creds):
    if creds.rank == Creds.Rank.ADMIN:
        print("dummy admin service", flush=True)
    elif creds.rank == Creds.Rank.USER:
        print("dummy user service", flush=True)
    elif creds.rank == Creds.Rank.GUEST:
        print("dummy guest service", flush=True)
    else:
        raise Exception("Invalid Rank")

if __name__ == "__main__":
    print("""\n\n
▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
█        ▀█▄▀▄▀██████ ▀█▄▀▄▀██████ 
  AuthLab  ▀█▄█▄███▀    ▀██▄█▄███▀
""", flush=True)
    
    dummy_service()
