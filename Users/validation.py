from Users.user import UserManager
import time, re #for checking email
from rich.console import Console
from rich.prompt import Prompt

class validService:
    def __init__(self):
        self.user_manager = UserManager()

    def is_valid_email(self, email):
        regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
        return re.match(regex, email)

    def are_valid_fields(self, Username, Password, Email=" "):
        if Username == "" or Password == "" or Email == "":
            raise ValueError('Please fill all fields.')
        elif len(Username) < 6: 
            raise ValueError('Username must be atleast 6 characters.')      
        elif " " in Username:
            raise ValueError('Username must not contain spaces.')      
        elif len(Password) < 8:
            raise ValueError('Password must be atleast 8 characters.')
        return True
            
    def sign_Up(self, Username, Password, Email):
        console = Console()
        try:
            self.are_valid_fields(Username, Password, Email)
            while not self.is_valid_email(Email):
                Email = Prompt.ask('Please enter a valid email: ')
                
            user = self.user_manager.add_user(Username, Password, Email)
            if user:
                console.print(f'You signed up successfully {Username}!', style='bold deep_sky_blue1')
                time.sleep(2.5)
                return user
            
        except ValueError as error:
            console.print(f'An error occured: {str(error)}', style='dark_orange')
            time.sleep(2.5)
            return None
    
    
    def log_in(self, Username, Password):
        console = Console()
        try:
            user = self.user_manager.load_user(Username, Password)
            if user:
                if user.is_Manager and user.activate:
                    console.print(f'Welcome back {Username}! \nYou logged in as manager.', style='bold deep_sky_blue1')
                    time.sleep(2.5)
                    return user            
                elif user.activate:
                    console.print(f'Welcome back {Username}!', style='bold deep_sky_blue1')
                    time.sleep(2.5)
                    return user
                elif not user.activate:
                    raise ValueError(f'{Username} is inactivated.')

        except FileNotFoundError as error:
            console.print(error, style='dark_orange')
        except ValueError as error:
            console.print(f'An error occured: {str(error)}', style='dark_orange')
            time.sleep(2.5)
        except Exception as error:
            console.print(f'An unexpected error occured: {str(error)}', style='dark_orange')
            time.sleep(2.5)
    
    
    def deactivate_user(self, Username, Password):
        console = Console()
        try:
            user = self.user_manager.load_user(Username, Password)
            if user:
                if user.activate:
                    user.activate = False
                    self.user_manager.save_user(user)
                    console.print(f'{Username} has been successfully deactivated.', style='bold deep_sky_blue1')
                    time.sleep(2.5)
                    return True
                else:
                    console.print(f'{Username} is already inactivated.', style='dark_orange')
                    time.sleep(2.5)
                    return False
                
        except ValueError as error:
            console.print(f'An error occured: {str(error)}', style='dark_orange')
            time.sleep(3.5)
        except FileNotFoundError as error:
            console.print(error, style='dark_orange')
            time.sleep(3.5)
            
    
    def activate_user(self, Username, Password):
        console = Console()
        try:
            user = self.user_manager.load_user(Username, Password)
            if user:
                if not user.activate:
                    user.activate = True
                    self.user_manager.save_user(user)
                    console.print(f'{Username} has been successfully activated.', style='bold deep_sky_blue1')
                    time.sleep(2.5)
                    return True
                else:
                    console.print(f'{Username} is already activated.', style='dark_orange')
                    time.sleep(2.5)
                    return False
        except ValueError as error:
            console.print(f'An error occured: {str(error)}', style='dark_orange')
            time.sleep(3.5)
        except FileNotFoundError as error:
            console.print(error, style='dark_orange')
<<<<<<< HEAD
            time.sleep(3.5)
=======
            time.sleep(3.5)
>>>>>>> ca95177 (Update Everything)
