from Users.user import UserManager
import os
import re #for checking email
import time

class validService:
    def __init__(self):
        self.user_manager = UserManager()

    def is_valid_email(self, email):
        regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
        return re.match(regex, email)

        
    def sign_Up(self, Username, Password, Email):
        while not self.is_valid_email(Email):
            Email = input('Please enter a valid email: ')
        try:
            user = self.user_manager.add_user(Username, Password, Email)
            print(f'You signed up successfully {Username}!')
            time.sleep(1.5)
            return user
        except ValueError as error:
            print(error)
            return None
    
    
    def log_in(self, Username, Password):
        user = self.user_manager.load_user(Username, Password)
        try:
            if user:
                if user.activate :
                    print(f'Welcome back {Username}!')
                    time.sleep(2)
                    return user
                else:
                    print(f'{Username} is inactivate.')
                    time.sleep(2)
            else:
                print('Invalid username or password.')
                time.sleep(2)
        except Exception as error:
            print(f'An unexpected error occured: {error}')
    
    
    def deactivate_user(self, Username, Password):
        user = self.user_manager.load_user(Username, Password)
        if user:
            user.active = False
            self.user_manager.save_users(user)
            print(f'{Username} has been successfully deactivated.')
            return user
        else:
            print('User not found.')
            return None
