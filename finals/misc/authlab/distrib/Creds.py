class Creds:
    PASSWORDS = {"admin" : "flag{placeholder}"}

    class Rank:
        GUEST = "Guest"
        USER  = "User"
        ADMIN = "Admin"
    
    def __init__(self, u, r):
        self.username = u
        self.rank     = r

    def __str__(self):
        return self.username + " (" + self.rank + ")"

    def isAdmin(self):
        False

    @classmethod
    def login(cls, username, password):
        if username == "admin":
            if cls.PASSWORDS.get(username) == password:
                return (True, Admin())
            else:
                return (False, "Incorrect password")
        elif username in cls.PASSWORDS:
            if cls.PASSWORDS.get(username) == password:
                return (True, User(username, password))
            else:
                return (False, "Incorrect password")
        else:
            return (False, "Invalid user. Sign up now!")

    @classmethod
    def signup(cls, username, password):
        assert username != "admin"
        assert len(password) >= 35
        if username in cls.PASSWORDS:
            return (False, "Username is not available")
        cls.PASSWORDS.update({username: password})
        return (True, User(username, password))

    @classmethod
    def guest(cls):
        return (True, Guest())

    @classmethod
    def isValidUsername(cls, u):
        return u not in cls.PASSWORDS

    @classmethod
    def storePassword(cls, u):
        cls.PASSWORDS.update({u.username: u.password})




class Guest(Creds):
    def __init__(self):
        super().__init__("anonymous", Creds.Rank.GUEST)

class Admin(Creds):
    def __init__(self):
        super().__init__("admin", Creds.Rank.ADMIN)
    
    def isAdmin(self):
        return True

class User(Creds):
    def __init__(self, u, p):
        super().__init__(u, Creds.Rank.USER)
        self.password = p
