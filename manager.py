import argparse #terminal management
import json 
import os
from pathlib import Path
from Users.user import User
from Users.user import UserManager
import hashlib



manager_file = Path('Data\\Manager.json')
users_file = Path('Data\\Users')
#project file
#task file

def create_admin(Username, Password):
    if find_manager(Username):
        print('Admin already exists.')
    elif os.path.getsize(manager_file) != 0:
        save_manager(Username, hash_password(Password))
        print('Admin updated successfully.')
    else:
        save_manager(Username, hash_password(Password))
        print('Admin created successfully.')


def find_manager(Username):
    try:
        with open(manager_file, 'r') as input:
            manager = json.load(input)
            if manager.get('Username') == Username:
                return True
            return False
    except Exception as error:
            print(f'There is an error: {error}')
            return False
    
def save_manager(Username, Password):
    try:
        user_manager = UserManager() #Save as user
        manager = User(Username, Password, " ", True)
        user_manager.user = manager
        user_manager.save_user()
        
        with open(manager_file, 'w') as output: #Save as manager
            json.dump({'Username' : Username, 'Password' : Password} , output)
    except Exception as error:
            print(f'There is an error: {error}')

def hash_password(password):         
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return hashed_password

            
        
def purge_data():
    confirmation = input('Are you sure you want to purge all data? (yes/no):')
    while True:
        try:
            if confirmation.lower() == 'yes':
                for data_path in [users_file #, project_file, #task_file 
                            ]:
                    for filename in os.listdir(data_path): #Get a list of all the files in the desired folder
                        file_path = os.path.join(data_path, filename)
                        os.unlink(file_path) #deleting the data
                    print('All data purged.')
            elif confirmation.lower() == 'no':
                print('Operation cancelled.')
            else:
                print('Please enter a valid answer.')
        except Exception as error:
            print(f'An uexpected error occured: {error}')
        break
        
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Project Management System")
    subparsers = parser.add_subparsers(dest='command')

    create_admin_parser = subparsers.add_parser('create-admin')
    create_admin_parser.add_argument('--username', required=True)
    create_admin_parser.add_argument('--password', required=True)
    purge_data_parser = subparsers.add_parser('purge-data')

    args = parser.parse_args()
    
    if args.command == 'create-admin':
        create_admin(args.username, args.password)
    elif args.command == 'purge-data':
        purge_data()
