import unittest
from Users.user import User, UserManager
import json
from pathlib import Path
import os

class TestUserManager(unittest.TestCase):

    def setUp(self):
        self.username = "yasaman"
        self.password = "mypassword123"
        self.email = "example@gmail.com"
        self.user_path = Path(f"Users_Data/Users/{self.username}.json")
        self.user_path.parent.mkdir(parents=True, exist_ok=True)

        self.manager = UserManager()
        self.user = self.manager.add_user(self.username, self.password, self.email)

    def test_check_password(self):
        with open(self.user_path, 'r') as f:
            user_data = json.load(f)
        
        saved_pass = user_data["Password"]
        self.assertTrue(self.user.check_password(saved_pass, self.password))

    def tearDown(self):
        if self.user_path.exists():
            os.remove(self.user_path)

        usernames_file = Path("Users_Data/Usernames.json")
        if usernames_file.exists():
            with open(usernames_file, 'r') as f:
                usernames = json.load(f)
            if self.username in usernames:
                usernames.remove(self.username)
            with open(usernames_file, 'w') as f:
                json.dump(usernames, f)

if __name__ == '__main__':
    unittest.main()
