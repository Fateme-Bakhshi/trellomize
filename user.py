import hashlib, os, json, time
from pathlib import Path #for file handling
from rich.console import Console

class User:
    def __init__(self, username, password, email, is_manager=False, active=True) :
        self.username = username
        self.password = self.hash_password(password)
        self.email = email
        self.activate = active
        self.is_Manager = is_manager
    
    @staticmethod    
    def hash_password(password):         
        """
        Hashes a password using SHA-256.
        
        Parameters
        ----------
        password : str
            The password to be hashed.
        
        Returns
        -------
        bytes
            The hashed password.
        """
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        return hashed_password

    def check_password(self, saved_pass, entered_pass):
        hashed_entered_pass = hashlib.sha256(entered_pass.encode('utf-8')).hexdigest()
        return saved_pass == hashed_entered_pass 
    
    def to_dict(self): #changing information to dictionary
        return{
                'Username': self.username,
                'Password': self.password,
                'Email' : self.email,
                'Active' : self.activate,
                'Manager' : self.is_Manager
            }
        
    
class UserManager:
    def __init__(self, data_files = 'Data\\Users'):
        self.data_file = Path(data_files)
        self.user = User('', '', '')
    
    def find_user(self, username):
        usernames_data = Path('Data/Usernames.json')
        if os.path.getsize(usernames_data) > 0:
            with open(usernames_data, 'r') as input:
                usernames = json.load(input)
            return username in usernames
        return False
    
    def add_user(self, username, password, email):
        console = Console()
        if self.find_user(username):
            console.print('\nUsername already exists.', style='dark_orange')
            time.sleep(2)
        else:
            self.user = User(username, password, email)
            self.save_user(self.user)
            return self.user
    
    def load_user(self, username, password):
        console = Console()
        try:
            the_user_data = self.data_file / f'{username}.json'
            with open(the_user_data, 'r') as input:
                data = json.load(input)
            
            the_username = data['Username']
            the_password = data['Password']
            email = data['Email']
            activate = data['Active']
            is_Manager = data['Manager']
            user = User(the_username, the_password, email, is_Manager, activate)
            
            if self.is_it_theUser(username, password):
                return user
            else:
                return None
        except Exception as error:
            console.print(f'There is an error: {error}', style='dark_orange')

        
    def save_user(self, user):
        try:
            the_user_data = self.data_file / f"{user.username}.json"
            usernames_data = Path('Data/Usernames.json')
            user_to_save = user.to_dict()
            
            with open(the_user_data, 'w') as output: #Saving the user
                json.dump(user_to_save, output)
            
            usernames = []
            if os.path.getsize(usernames_data) > 0:
                with open(usernames_data, 'r') as names: #Reading the usernames
                    usernames = json.load(names)
                if not(user.username in usernames):
                    usernames.append(user.username)
            
            with open(usernames_data, 'w') as name: #Saving updated usernames
                json.dump(usernames, name)
                
        except Exception as error:
            print(f'An error occured: {error}')
            
            
    def is_it_theUser(self, username, password):
        is_it_thePass = self.user.check_password(self.user.password, password)
        is_it_theUserN = True if self.user.username == username else False
        return is_it_theUserN == is_it_thePass
