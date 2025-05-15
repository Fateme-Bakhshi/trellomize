import hashlib, os, json, re
from pathlib import Path #for file handling

usernames_file = Path('Users_Data/Usernames.json')

class User:
    def __init__(self, username, password, email, is_manager=False, active=True) :
        self.username = username
        self.password = self.hash_password(password)
        self.email = email
        self.activate = active
        self.is_Manager = is_manager
      
    def hash_password(self, password):         
        """
        Hashes a password using SHA-256 if it's not hashed already.
        
        Parameters
        ----------
        password : str
            The password to be hashed.
        
        Returns
        -------
        bytes
            The hashed password.
        """
        if len(password) == 64 and re.match(r'^[a-f0-9]{64}$', password):
            return password
        else:
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
    def __init__(self, data_files = 'Users_Data\\Users'):
        self.data_file = Path(data_files)
        self.user = User('', '', '')
    
    def find_user(self, username):
        if os.path.exists(usernames_file) > 0:
            with open(usernames_file, 'r') as input:
                usernames = json.load(input)
            return username in usernames
        return False
    
    def add_user(self, username, password, email):
        if self.find_user(username):
            raise ValueError('Username already exists.')
        else:
            user = User(username, password, email)
            self.save_user(user)
            return user
    
    def load_user(self, username, password):
        try:
            the_user_data = self.data_file / f'{username}.json'
            if os.path.exists(the_user_data):
                with open(the_user_data, 'r') as input:
                    data = json.load(input)
                    
                saved_username = data['Username']
                saved_password = data['Password']
                
                if self.is_it_theUser(username, password, saved_username, saved_password):
                    saved_email = data['Email']
                    activate = data['Active']
                    is_Manager = data['Manager']
                    user = User(saved_username, saved_password, saved_email, is_Manager, activate)
                    return user
                else:
                    raise ValueError('Invalid username or password.')
            else: 
                raise FileNotFoundError(f'User data file not found for "{username}".')
        except ValueError as error:
            raise ValueError(error)
        

        
    def save_user(self, user):
        try:
            the_user_data = self.data_file / f"{user.username}.json"
            user_to_save = user.to_dict()
            
            with open(the_user_data, 'w') as output: #Saving the user
                json.dump(user_to_save, output)
                
            usernames = []
            if os.path.exists(usernames_file) > 0:
                with open(usernames_file, 'r') as names: #Reading the usernames
                    usernames = json.load(names)
            if not(user.username in usernames):
                usernames.append(user.username)
            
            with open(usernames_file, 'w') as name: #Saving updated usernames
                json.dump(usernames, name)
        except ValueError:
            raise('Could not open files.')
            
            
    def is_it_theUser(self, username, password, saved_username, saves_password):
        is_it_thePass = self.user.check_password(saves_password, password)
        is_it_theUserN = saved_username== username 
<<<<<<< HEAD
        return (is_it_theUserN and is_it_thePass)
=======
        return (is_it_theUserN and is_it_thePass)
>>>>>>> ca95177 (Update Everything)
