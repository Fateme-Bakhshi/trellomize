from Users.validation import validService
import os, time, sys #for show_slowly func
from rich.markdown import Markdown
from rich.console import Console
from rich.prompt import Prompt
from rich import print
from rich.panel import Panel


class main:
    def __init__(self):
        self.valid_service = validService()
        self.user = {}
    
    def clear_screen(self):
        os.system('cls')
        
    def print_slowly(self, text, delay=0.1):
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush() 
            time.sleep(delay)
        time.sleep(1.5)
    
    def show_title(self, title):
        self.clear_screen()
        console = Console()
        print('\n')
        console.rule(title, style="bold white")
        time.sleep(1)
    
    def display_choices(self, choices, width):
        console = Console()
        for option, title in enumerate(choices):
            console.print(Panel(title,title=str(option+1),title_align="center", width=width, border_style="bold deep_sky_blue1"), justify="center")
            time.sleep(0.2)
    
    def exit_program(self):
        self.clear_screen()
        self.print_slowly("\nThanks for using this program!", 0.04)
        time.sleep(0.5)
        exit(1)
    
    def back_or_continue(self):
        console = Console()
        choices = ['Continue', 'Back']
        self.display_choices(self, choices, 12)
        choice = input()
        while True:
            if choice == '0' or choice == '1':
                return int(choice)
            else:
                choice = input('Please enter a valid number(0 or 1): ')
                    
    def log_or_sign(self):
        self.clear_screen()
        
        self.print_slowly("\nWelcome to Project Management System!", 0.04)
        
        while True:
            self.show_title("[bold deep_sky_blue1]Login/Sign Up")
            print("\n")
            self.display_choices(['Login', 'Sign Up', 'Exit'], 12)
            choice = input("                                                                      Enter your choice: ")
              
            while True:
                if(choice == '1'):
                    self.login()
                    break
                elif(choice == '2'):
                    self.sign_up()
                    break
                elif(choice == '3'):
                    self.exit_program()
                else:
                    choice = input("                                                             Please enter a valid number(1-3): ")
        
    def login(self):
        self.show_title("[bold deep_sky_blue3]Login")
        
        username = Prompt.ask("Enter your Username")
        password = Prompt.ask("Enter your Password", password=True)
        print('\n')
        self.user = self.valid_service.log_in(username, password)
        if self.user:
            self.user_dashboard()
        else:
            if self.back_or_continue():
                self.login()
        
    def sign_up(self):
        self.show_title("[bold deep_sky_blue3]Sign Up")
        
        username = Prompt.ask("Enter the Username")
        password = Prompt.ask("Enter the Password", password=True)
        email = Prompt.ask("Enter the Email", default="example@gmail.com")
        print('\n')
        
        user = self.valid_service.sign_Up(username, password, email)
        if not user:
            if self.back_or_continue():
                self.sign_up()
            
    
    def user_dashboard(self):
        while True:
            self.show_title("[bold deep_sky_blue3]User Dashboard")
            print("\n")
        
            choices = ['Pre-made projects', 'Making a new project']
            if not self.user.is_Manager:
                choices.extend(['Back', 'Exit'])
                self.display_choices(choices, 20)
            else:
                choices.extend(['Deactivating an account', 'Activating an account', 'Back', 'Exit'])
                self.display_choices(choices, 20)
            

            choice2 = input('                                                                     Enter your choice: ')
            while True:
                if (choice2 == '3' and not self.user.is_Manager):
                    return
                if (choice2 == '4' and not self.user.is_Manager):
                    self.exit_program()
                if (choice2 == '3' and self.user.is_Manager):
                    self.deactivating_user()
                    break
                if (choice2 == '4' and self.user.is_Manager):
                    self.activating_user()
                    break
                if (choice2 == '5' and self.user.is_Manager):
                    return
                if (choice2 == '6' and self.user.is_Manager):
                    self.exit_program()
                else:
                    choice2 = input('                                                                  Please enter a valid number: ')
                
    def deactivating_user(self):
        self.show_title("[bold deep_sky_blue3]Deactivating User")
        
        username = Prompt.ask('Enter the userename you want to deactivate')
        password = Prompt.ask('Enter the password of the account', password=True)
        print('\n')
        self.valid_service.deactivate_user(username, password)

    def activating_user(self):
        self.show_title("[bold deep_sky_blue3]Activating User")
        
        username = Prompt.ask('Enter the userename you want to activate')
        password = Prompt.ask('Enter the password of the account', password=True)
        print('\n')
        self.valid_service.activate_user(username, password)
        
        
if __name__ == "__main__":
    m = main()
    m.log_or_sign()
    
#python mainn.py
