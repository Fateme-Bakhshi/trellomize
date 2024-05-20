import hashlib
import os
import json
from pathlib import Path #for file handling

class User:
    def __init__(self, username, password, email, active=True) :
        self.username = self.username
        self.password = self.hash_password(password)
        self.email = email
        self.activate = active
    
    @staticmethod    
    def hash_password(password):         
        """
        Hashes a password using SHA-256 with a random salt.
        
        Parameters
        ----------
        password : str
            The password to be hashed.
        
        Returns
        -------
        bytes
            The salt concatenated with the hashed password.
        """
        salt = os.urandom(16)
        hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
        
        return salt + hashed_password
    
    def to_dic(self): #changing information to dictionary
        return
        {
            'Username': self.username,
            'Password': self.password,
            'Email' : self.email,
            'Active' : self.activate
        }
        
    @staticmethod
    def pre_users(data): #Initialization previous users
        PreUser = User(data['Username'], data['Password'], data['Email'], data['Active'])
        return PreUser
    
class UserManager:
    def __init__(self, data_files = 'Data\\Users'):
        self.data_file = Path(data_files)
        self.user = self.load_user()
    
    def find_user(self, username):
        usernames_data = self.data_files / 'Usernames.json'
        with open(usernames_data, 'r') as input:
            usernames = input.read().split()
        return username in usernames
    
    def load_user(self, username, password):
        if self.is_it_theaUser(username, password):
            try:
                the_user_data = self.data_file / f'{username}.json'
                with open(the_user_data, 'r') as input:
                    return json.load(input)
            except Exception as error:
                print(f'There is an error: {error}')
        else:
            return None
        
    def save_user(self, user):
        try:
            the_user_data = self.data_file / f'{user.get('Username')}.json'
            with open(the_user_data, 'w') as output:
                json.dump(output)
        except Exception as error:
            print(f'An error occured: {error}')
            
    def add_user(self, username, password, email):
        if self.find_user(username):
            raise ValueError('Username already exists.')
        else:
            user = User(username, password, email)
            user = user.to_dic()
            self.user = user
            self.save_user(self)
            return user
            
    def is_it_theUser(self, username, password):
        return self.user.get('Username') == username and self.user.get('Password') == password
            
    
