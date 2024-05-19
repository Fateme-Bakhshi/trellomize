import argparse #terminal management
import json 
from pathlib import Path

manager_file = Path('Data\\Manager.json')
users_file = Path('Data\\Users.json')
#project file
#task file

def create_admin(Username, Password):

    if find_manager(Username):
        print('Admin already exists.')
    else:
        print('Admin created successfully.')
        save_manager(Username, Password)


def find_manager(Username):
    try:
        with open(manager_file, 'r') as input:
            manager = json.load(input)
            if manager[0].get('username') == Username:
                return True
            return False
    except Exception as error:
            print(f'There is an error: {error}')
            return False
    
def save_manager(Username, Password):
    try:
        with open(manager_file, 'w') as output:
            json.dump([{'username' : Username, 'password' : Password}] , output)
    except Exception as error:
            print(f'There is an error: {error}')
            
        
        
        
def purge_data():
    confirmation = input('Are you sure you want to purge all data? (yes/no):')
    try:
        if confirmation.lower() == 'yes':
            for data_path in [users_file #, project_file, #task_file 
                        ]:
                with open(data_path, 'w') as f:
                    f.write('[]')
                print('All data purged.')
        elif confirmation.lower() == 'no':
            print('Operation cancelled.')
        else:
            print('Please enter a valid answer.')
            purge_data()
    except Exception as error:
        print(f'An uexpected error occured: {error}')
        
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Project Management System Manager")
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