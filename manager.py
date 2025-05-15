import argparse #terminal management
import json , os, logging
from pathlib import Path
from Users.user import User
from Users.user import UserManager
from Users.validation import validService

logging.basicConfig(filename="logFile/actions.log", format='%(asctime)s - %(message)s', filemode='a', level=logging.DEBUG)

usernames_file = Path('Users_Data/Usernames.json')
manager_file = Path('Users_Data\\Manager.json')
users_file = Path('Users_Data\\Users')
project_file = Path('Projects_Data')
logfile = Path('logFile/actions.log')

def create_admin(Username, Password):
    valid_service = validService()
    try:
        if valid_service.are_valid_fields(Username, Password):
            if find_manager(Username):
                print('Admin already exists.')
            elif os.path.exists(manager_file):
                update_manager(Username, Password)
                print('Admin updated successfully.')
                logging.info(f'Manager updated to "{Username}".')
            else:
                save_manager(Username, Password)
                print('Admin created successfully.')
                logging.info(f'"{Username}" was created as a Manager.')
    except ValueError as error:
        print(f'There is an error: {error}')


def find_manager(Username):
    try:
        if os.path.exists(manager_file):
            with open(manager_file, 'r') as input:
                manager = json.load(input)
                if manager['Username'] == Username:
                    return True
        return False
    except Exception as error:
            print(f'There is an error: {str(error)}')
            return False
    
def save_manager(Username, Password):
    try:
        user_manager = UserManager() #Save as user
        manager = User(Username, Password, " ", True)
        user_manager.save_user(manager)
        
        with open(manager_file, 'w') as output: #Save as manager
            user_to_save = manager.to_dict()
            json.dump(user_to_save , output)
    except Exception as error:
            print(f'There is an error: {error}')

def update_manager(Username, Password):
    """
    Updates the current manager,
    deletes the previous manager saved as 'user' and it's username,
    and saves the new manager.
    
    Parameters
    ----------
    Username, Password : str
        the manager's username and password
    """
    with open(manager_file, 'r') as input: 
        manager = json.load(input)
        manager_username = manager['Username'] 
    manager_as_user = Path(f'Uses_Data\\Users/{manager_username}.json')
    os.unlink(manager_as_user)
    
    usernames = []
    if os.path.exists(usernames_file):
        with open(usernames_file, 'r') as names: #Reading the usernames
            usernames = json.load(names)
        usernames.remove(manager_username)
    with open(usernames_file, 'w') as name: #Saving updated usernames
        json.dump(usernames, name)
        
    save_manager(Username, Password)
    

def purge_data():
    confirmation = input('Are you sure you want to purge all data? (yes/no):')
    while True:
        try:
            if confirmation.lower() == 'yes':
                for data_path in [users_file, project_file]:
                    for filename in os.listdir(data_path): #Get a list of all the files in the desired folder
                        file_path = os.path.join(data_path, filename)
                        os.unlink(file_path) #deleting the data
                if usernames_file.exists():
                    os.remove(usernames_file)
                if manager_file.exists():
                    os.remove(manager_file)
                if logfile.exists():
                    logging.shutdown()
                    os.remove(logfile)
                print('All data purged.')
                break
            elif confirmation.lower() == 'no':
                print('Operation cancelled.')
                break
            else:
                confirmation = input('Please enter a valid answer.')
                
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
<<<<<<< HEAD
        purge_data()
=======
        purge_data()
>>>>>>> ca95177 (Update Everything)
