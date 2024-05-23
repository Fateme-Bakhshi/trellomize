import hashlib
import os
import json
from pathlib import Path #for file handling
import time

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
        usernames_data = Path(self.data_file / 'Usernames.json')
        if os.path.getsize(usernames_data) > 0:
            with open(usernames_data, 'r') as input:
                usernames = json.load(input)
            return username in usernames
        return False
    
    def add_user(self, username, password, email):
        if self.find_user(username):
            print('Username already exists.')
            time.sleep(2)
        else:
            self.user = User(username, password, email)
            self.save_user()
            return self.user
    
    def load_user(self, username, password):
        try:
            the_user_data = self.data_file / f'{username}.json'
            with open(the_user_data, 'r') as input:
                data = json.load(input)
                
            self.user.username = data['Username']
            self.user.password = data['Password']
            self.user.email = data['Email']
            self.user.activate = data['Active']
            self.user.is_Manager = data['Manager']
            
            if self.is_it_theUser(username, password):
                return self.user
            else:
                return None
        except Exception as error:
            print(f'There is an error: {error}')

        
    def save_user(self):
        try:
            the_user_data = self.data_file / f"{self.user.username}.json"
            usernames_file = self.data_file / "Usernames.json"
            user_to_save = self.user.to_dict()
            
            with open(the_user_data, 'w') as output: #Saving the user
                json.dump(user_to_save, output)
            
            usernames = []
            if os.path.getsize(usernames_file) > 0:
                with open(usernames_file, 'r') as names: #Reading the usernames
                    usernames = json.load(names)
            usernames.append(self.user.username)
            
            with open(usernames_file, 'w') as name: #Saving updated usernames
                json.dump(usernames, name)
                
        except Exception as error:
            print(f'An error occured: {error}')
            
            
    def is_it_theUser(self, username, password):
        is_it_thePass = self.user.check_password(self.user.password, password)
        is_it_theUserN = True if self.user.username == username else False
        return is_it_theUserN == is_it_thePass
