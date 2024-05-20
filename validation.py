from Users.user import UserManager
import re #for checking email

class validService:
    def __init__(self):
        self.user_manager = UserManager
    
    def is_valid_email(Email):
        regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

        if re.match(regex, Email):
            return True
        else:
            return False
        
    def sign_Up(self, Username, Password, Email):
        while True:
            if(self.is_valid_email(Email)):
                try:
                    user = self.user_manager.add_user(Username, Password, Email)
                    print(f'You signed up successfully {Username}!')
                    return user
                except ValueError as error:
                    print(error)
            else:
                print('Please enter a valid email.')
    
    def log_in(self, Username, Password):
        user = self.user_manager.load_user(Username, Password)
        while True:
            try:
                if user:
                    if user.active :
                        print(f'Welcome back {Username}!')
                        return user
                    else:
                        print(f'{Username} is inactivate.')
                else:
                    print('Invalid username or password.')
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
