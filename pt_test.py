import unittest
from Users.user import User
import json

class TestUserManager(unittest.TestCase):
    
    def testcheck_password(self):
        user = User("yasaman" , "ef797c8118f02dfb649607dd5d3f8c7623048c9c063d532cc95c5ed7a898a64f" , "example@gmail.com")
        with open ('Users_Data\\Users/yasaman.json' , 'r') as f:
            user1 = json.load(f)
        saved_pass = user1["Password"]
        hashed_pass = "ef797c8118f02dfb649607dd5d3f8c7623048c9c063d532cc95c5ed7a898a64f"
        self.assertFalse(user.check_password(saved_pass , hashed_pass))
        return saved_pass == hashed_pass 


if __name__ == '__main__':
    unittest.main()
