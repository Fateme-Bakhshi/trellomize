from Users.validation import validService
import os
from rich.markdown import Markdown
from rich.console import Console
from rich.prompt import Prompt
from rich import print
from rich.panel import Panel
import time
import sys

class main:
    def __init__(self):
        self.valid_service = validService()
        self.user = {}
        
    def show_slowly(self, text, delay=0.1):
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush() 
            time.sleep(delay)
    
    def title(self, con, text):
        os.system('cls')
        print("\n")
        con.rule(text, style="bold white")
            
    def log_or_sign(self):
        os.system('cls')
        con = Console()
        
        self.show_slowly("\nWelcome to Project Management System!", 0.04)
        time.sleep(2)
        
        while True:
            self.title(con, "[bold deep_sky_blue3]Login/Sign Up")
            print("\n")
            con.print(Panel("Login",title="1",title_align="center", width=12, border_style="bold deep_sky_blue1"), justify="center")
            time.sleep(0.2)
            con.print(Panel("Sign Up",title="2",title_align="center", width=12, border_style="bold deep_sky_blue1"), justify="center")
            time.sleep(0.2)
            con.print(Panel("Exit",title="3",title_align="center", width=12, border_style="bold deep_sky_blue1"), justify="center")
            time.sleep(0.2)
            
            choice = input("                                                          Enter your choice: ")
            
            while True:
                if(choice == '1'):
                    self.login()
                    break
                elif(choice == '2'):
                    self.sign_up()
                    break
                elif(choice == '3'):
                    os.system('cls')
                    self.show_slowly("\nThanks for using this program!", 0.04)
                    time.sleep(0.5)
                    exit(1)
                else:
                    choice = input("                                                   Please enter a valid number(1-3): ")
        
    def login(self):
        con = Console()
        self.title(con, "[bold deep_sky_blue3]Login")
        time.sleep(1)
        
        username = Prompt.ask("Enter your Username")
        password = Prompt.ask("Enter your Password")
        self.user = self.valid_service.log_in(username, password)
        if self.user:
            self.user_dashboard()
        
    def sign_up(self):
        con = Console()
        self.title(con, "[bold deep_sky_blue3]Sign Up")
        time.sleep(1)
        
        username = Prompt.ask("Enter the Username")
        password = Prompt.ask("Enter the Password")
        email = Prompt.ask("Enter the Password", default="example@gmail.com")
        
        self.valid_service.sign_Up(username, password, email)
    
    def user_dashboard(self):
        con = Console()
        self.title(con, "[bold deep_sky_blue3]User Dashboard")
        print("\n")
        time.sleep(1)
        
        con.print(Panel("Pre-made projects",title="1",title_align="center", width=20, border_style="bold deep_sky_blue1"), justify="center")
        time.sleep(0.2)
        con.print(Panel("Making a new project",title="2",title_align="center", width=20, border_style="bold deep_sky_blue1"), justify="center")
        time.sleep(0.2)
        if self.user.is_Manager:
            con.print(Panel("Deactivating an account",title="3",title_align="center", width=20, border_style="bold deep_sky_blue1"), justify="center")
            time.sleep(0.2)
            con.print(Panel("Activating an account ",title="4",title_align="center", width=20, border_style="bold deep_sky_blue1"), justify="center")
            time.sleep(0.2)
            
        input = ('Enter your choice: ')
        exit(1)

if __name__ == "__main__":
    m = main()
    m.log_or_sign()
    
#python mainn.py