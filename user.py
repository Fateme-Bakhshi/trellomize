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
    def __init__(self, data_file = 'Data\\Users.json'):
        self.data_file = Path(data_file)
        self.users = self.load_users()
    
    def find_user(self, Username):
        for user in self.users:
            if user == Username:
                return user
        return None
        
    def load_users(self):
        try:
            with open(self.data_file, 'r') as input:
                return [User.pre_users(user) for user in json.load(input)]
        except Exception as error:
            print(f'There is an error: {error}')
            return []
    
    def save_user(self):
        try:
            with open(self.data_file(), 'w') as output:
                json.dump([user.to_save() for user in self.users] , output)
        except Exception as error:
            print(f'There is an error: {error}')
    
    def add_user(self, Username, Password, Email):
        if self.find_user():
            raise ValueError('Username already exists. Please enter a new one.')
        user = User(Username, Password, Email)
        self.users.append(user)
        self.save_user()