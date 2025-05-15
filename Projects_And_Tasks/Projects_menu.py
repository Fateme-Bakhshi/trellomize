from .task import TaskManager
from .task import TableTask
from .project import ProjectManager
<<<<<<< HEAD
import json #for save file
from pathlib import Path  #for save file
import os, logging, time, sys
from rich.console import Console
from Users.user import UserManager
=======
import shutil, json #for save file
from pathlib import Path  #for save file
import os, logging, time
from rich.console import Console
from Users.user import UserManager
from rich.table import Table
>>>>>>> ca95177 (Update Everything)

logging.basicConfig(filename="logFile/actions.log", format='%(asctime)s - %(message)s', filemode='a', level=logging.DEBUG)

def clear_screen():
    os.system('cls')
    

def show_title(title):
    clear_screen()
    console = Console()
    print('\n')
    console.rule(title, style="bold white")
<<<<<<< HEAD
    #time.sleep(1)
    
def back():
    choice = input('[0]Back\n')
=======
    time.sleep(1)

def get_choice(text):
    columns = shutil.get_terminal_size().columns
    spaces = (columns - len(text)) // 2
    print(' ' * spaces + text, end="")
    choice = input()
    return choice

def back():
    choice = input('\n[0]Back\n')
>>>>>>> ca95177 (Update Everything)
    while True:
        if choice == '0':
            return True
        else:
            choice = input('Enter "0" to return: ')

def DisplayAllProject(projectManager , projects , Isbool , username):
    """Show all proejcts

    Args:
        projectManager (_type_): _object or dict of project_
        projects (_type_): _projects_
        Isbool (_type_): _bool_
        username (_type_): _username_
    """
<<<<<<< HEAD
    clear_screen()
    try:
        print("Project List:")
        if len(projects) == 0:
            print("There are no projects.")
            return
        temp = 0
        it = 0
        for it in range(len(projects)):
            temp += 1
            print(f"({int(it) + 1}.{projects[it]['title']} / ID: {projects[it]['id']})")
        choice = input("\nWhich one you choose? ")
        while True:
            if int(choice) > int(temp) and int(choice) <= 0:
                print("Invalid choice.Pleas try again.")
                choice = input()
            else:
                if Isbool == False:
                    project = projects[int(choice) - 1]
                    TableTask(project["tasks"] , username , project["id"])
                    break
                elif Isbool == True:
                    project = projects[int(choice) - 1]
                    ProjectMenu(projectManager , project , username)
                    break
    except Exception as e:
        print(f"Error Displaying all projecst: {e}")
=======
    console = Console()
    try:
        print("Project List:")
        if len(projects) == 0:
            print("There are no projects yet.")
            return
        
        project_table = Table(show_header=True, header_style="bold deep_sky_blue1")
        project_table.add_column("Number", style="dim", width=12)
        project_table.add_column("Title", style="dim", width=12)
        project_table.add_column("ID", style="dim", width=12)
        
        temp = 0
        for project in projects:
            project_table.add_row(str(temp+1), project['title'], str(project['id']))
            temp += 1
        console.print(project_table)
        print('[0]None of them.')
        choice = input("\nWhich one do you choose?(Enter the number): ")
        while True:
            choice = int(choice)
            if choice > temp+1 or choice < 0:
                console.print("\nInvalid choice.Please try again: ", style='dark_orange')
                choice = input()
                choice = int(choice)
            if choice == 0:
                return
            else:
                if Isbool == False:
                    project = projects[choice - 1]
                    TableTask(project["tasks"] , username , project["id"])
                    break
                elif Isbool == True:
                    project = projects[choice - 1]
                    ProjectMenu(projectManager , project , username)
                    break
    except Exception as e:
        console.print(f"\nError Displaying all projecst: {e}", style='dark_orange')
>>>>>>> ca95177 (Update Everything)




def ProjectMenu(projectManager , project , username):
    """Menu for project and tasks

    Args:
        projectManager (_type_): _description_
        project (_type_): _description_
        username (_type_): _description_
    """
<<<<<<< HEAD
    while True:
        time.sleep(5)
        clear_screen()
        print("\n")
=======
    console = Console()
    while True:
        show_title(f'[bold deep_sky_blue3]Project "{project["title"]}"')
>>>>>>> ca95177 (Update Everything)
        print("[1] View members")##member in each project
        print("[2] View Tasks")##all of task in each project
        print("[3] View Leader")## show username of leader of each project
        print("[4] View tasks assigned to a member")##all task in each project that assigned to a member
        if username == project["leader"]:
            print("[5] Add a member to the project")
            print("[6] Remove a member from the project")
            print("[7] Deleting the project")
            print("[8] Add task to project")
            print("[9] Back to main menu")
        else:
            print("[5] Back to main menu")
        choice = input("\nEnter your choice: ")
        if choice == '1':
<<<<<<< HEAD
            if len(project["members"]) == 0:
                print("This project doesn't have any member")
            else:
                i = 0
                print("Members:")
                for i in range(len(project["members"])):
                    print(f"{int(i + 1)}. {project['members'][i]}")

        elif choice == '2':
            if len(project["tasks"]) == 0:
                print("There is no task yet")
            else:
                i = 0
                print("Tasks:")
                for i in range(len(project["tasks"])):
                    print(f"{int(i + 1)}]")
                    print(f' Title: {project["tasks"][i]["title"]}')
                    print(f' ID: {project["tasks"][i]["id"]}')
                    print(f' Description: {project["tasks"][i]["description"]}')
                    print(f' Assigners: {",".join(project["tasks"][i]["assigners"])}')
                    print(f' Start Time: {project["tasks"][i]["startTime"]}')
                    print(f' End Time: {project["tasks"][i]["endTime"]}')
                    print(f' Priority: {project["tasks"][i]["priority"]}')
                    print(f' Status: {project["tasks"][i]["status"]}')
                    print(" History:")
                    for it in range(len(project["tasks"][i]["history"])):
                        print(f'{int(it) + 1}.')
                        print(f'  User : {project["tasks"][i]["history"][it]["user"]}')
                        print(f'  Description : {project["tasks"][i]["history"][it]["action"]}')
                    print(" Comments:")
=======
            show_title(f'[bold deep_sky_blue3]Members of Project "{project["title"]}"')
            if len(project["members"]) == 0:
                console.print("\nThis project doesn't have any member", style='dark_orange')
            else:
                print("Members:")
                for i in range(len(project["members"])):
                    print(f"{int(i + 1)}. {project['members'][i]}")
            if back():
                time.sleep(0.2)

        elif choice == '2':
            show_title(f'[bold deep_sky_blue3]Tasks of Project "{project["title"]}"')
            if len(project["tasks"]) == 0:
                print("There are no tasks yet.")
            else:
                print("\nTasks:")
                for i in range(len(project["tasks"])):
                    print(f'{[i + 1]}')
                    console.print("[bold deep_sky_blue1]ID: [/bold deep_sky_blue1][bold white]{}".format(project["tasks"][i]["id"]), style="bold white")
                    print("." * 40)
                    console.print("[bold deep_sky_blue1]Title: [/bold deep_sky_blue1][bold white]{}".format(project["tasks"][i]["title"]), style="bold white")
                    print("." * 40)
                    console.print("[bold deep_sky_blue1]Description: [/bold deep_sky_blue1][bold white]{}".format(project["tasks"][i]["description"]), style="bold white")
                    print("." * 40)
                    console.print("[bold deep_sky_blue1]Priority: [/bold deep_sky_blue1][bold white]{}".format(project["tasks"][i]["priority"]), style="bold white")
                    print("." * 40)
                    console.print("[bold deep_sky_blue1]Status: [/bold deep_sky_blue1][bold white]{}".format(project["tasks"][i]["status"]), style="bold white")
                    print("." * 40)
                    console.print("[bold deep_sky_blue1]Start Time: [/bold deep_sky_blue1][bold white]{}".format(project["tasks"][i]["startTime"]), style="bold white")
                    print("." * 40)
                    console.print("[bold deep_sky_blue1]End Time: [/bold deep_sky_blue1][bold white]{}".format(project["tasks"][i]["endTime"]), style="bold white")
                    print("." * 40)
                    console.print("[bold deep_sky_blue1]Assigners: [/bold deep_sky_blue1][bold white]{}".format(project["tasks"][i]["assigners"]), style="bold white")
                    print("." * 40)
                    console.print("History:", style='deep_sky_blue1')
                    for it in range(len(project["tasks"][i]["history"])):
                        print(f"{int(it) + 1}.")
                        print(f'  User : {project["tasks"][i]["history"][it]["user"]}')
                        print(f'  Description : {project["tasks"][i]["history"][it]["action"]}')
                        if len(project["tasks"][i]["history"]) > 1:
                            print("." * 15)
                    print("." * 40)
                    console.print("Comments:", style='deep_sky_blue1')
>>>>>>> ca95177 (Update Everything)
                    for j in range(len(project["tasks"][i]["comments"])):
                        print(f"{int(j) + 1}.")
                        print(f'  User : {project["tasks"][i]["comments"][j]["user"]}')
                        print(f'  Description : {project["tasks"][i]["comments"][j]["description"]}')
<<<<<<< HEAD
        elif choice == '3':
            print(f'Leader: {project["leader"]}')

        elif choice == '4':
=======
                        if len(project["tasks"][i]["comments"]) > 1:
                            print("." * 15)
                    print("─" * 60)

            if back():
                time.sleep(0.2)
            
        elif choice == '3':
            show_title(f'[bold deep_sky_blue3]Leader of Project "{project["title"]}"')
            print(f'Leader: {project["leader"]}')
            time.sleep(4)

        elif choice == '4':
            show_title('[bold deep_sky_blue3]Tasks assigned to a member')
>>>>>>> ca95177 (Update Everything)
            if len(project["tasks"]) == 0:
                print("There are no tasks yet.")
            else:
                member = input("Enter username of member: ")
                i = 0
                temp = 0
                for i in range(len(project["tasks"])):
                    if member in project["tasks"][i]["assigners"]:
                        temp += 1
<<<<<<< HEAD
                        print(f'{member} assigned to this task {project["tasks"][i]["title"]}')
                if temp == 0:
                    print(f'{username} is assigned to no tasks')

        elif username != project["leader"] and choice == '5':
            return

        elif choice == '5' and username == project["leader"]:
            clear_screen()
            user_manager = UserManager()
            Adduser = input("Enter the ID you want to add: ")
            if not user_manager.find_user(Adduser):
                print('Username does not exist.')
            else:
                projectManager.AddMember(project["id"] , project["title"] , Adduser , username)
        
        elif choice == '6' and username == project["leader"]:
            clear_screen()
            removeuser = input("Enter the ID you want to remove: ")
            projectManager.RemoveMember(project["id"] , project["title"] , removeuser , username)

        elif choice == '7' and username == project["leader"]:
            projectManager.DeletProject(project["id"] , project["title"] , username)
=======
                        console.print(f'\n{member} assigned to this task {project["tasks"][i]["title"]}', style='bold deep_sky_blue1')
                if temp == 0:
                    console.print(f'\n{username} is assigned to no tasks', style='dark_orange')
            if back():
                time.sleep(0.2)
            
        elif username != project["leader"] and choice == '5':
            return


        elif choice == '5' and username == project["leader"]:
            show_title(f'[bold deep_sky_blue3]Add a member to the "{project["title"]}"')
            user_manager = UserManager()
            Adduser = input("Enter the ID you want to add: ")
            if not user_manager.find_user(Adduser):
                console.print('\nUsername does not exist.', style='dark_orange')
            else:
                projectManager.AddMember(project["id"] , project["title"] , Adduser , username)
            time.sleep(3)
        
        elif choice == '6' and username == project["leader"]:
            show_title(f'[bold deep_sky_blue3]Remove a member of "{project["title"]}"')
            removeuser = input("Enter the ID you want to remove: ")
            projectManager.RemoveMember(project["id"] , project["title"] , removeuser , username)
            time.sleep(4)

        elif choice == '7' and username == project["leader"]:
            projectManager.DeletProject(project["id"] , project["title"] , username)
            time.sleep(4)
            break
>>>>>>> ca95177 (Update Everything)

        elif choice == '8' and username == project["leader"]:
            taskManager = TaskManager()
            taskManager.CreatTask(project["id"])
<<<<<<< HEAD
=======
            time.sleep(4)
>>>>>>> ca95177 (Update Everything)

        elif choice == '9' and username == project["leader"]:
            return
        else:
<<<<<<< HEAD
            print("Invalid choice.Please try again.")
=======
            console.print("\nInvalid choice.Please try again.", style='dark_orange')
>>>>>>> ca95177 (Update Everything)


def Main(choice, username):
    projectManager = ProjectManager()
    AllprojectFile = Path('Projects_Data/project.json')
    print("\n")
    while True:
        if choice == '1':
<<<<<<< HEAD
            show_title('Member Projects')
=======
            clear_screen()
            show_title('[bold deep_sky_blue3]Member Projects')
>>>>>>> ca95177 (Update Everything)
            projectManager.MemeberProject(username)
            if back():
                break
        
        elif choice == '2':
<<<<<<< HEAD
            show_title('Leader Projects')
=======
            clear_screen()
            show_title('[bold deep_sky_blue3]Leader Projects')
>>>>>>> ca95177 (Update Everything)
            projectManager.LeaderProjects(username)
            if back():
                break
        
        elif choice == '3':
<<<<<<< HEAD
            clear_screen()
            show_title('Managing Tasks')
            with open(AllprojectFile , 'r') as f:
                AllProjects = json.load(f)
            DisplayAllProject(projectManager , AllProjects , False , username)
            if back():
                break

        elif choice == '4':
            show_title('Managing Projects')
            with open(AllprojectFile , 'r') as f:
                AllProjects = json.load(f)
            DisplayAllProject(projectManager , AllProjects , True , username)
            if back():
                break
=======
            show_title('[bold deep_sky_blue3]Managing Tasks')
            
            if os.path.exists(AllprojectFile):
                with open(AllprojectFile , 'r') as f:
                    AllProjects = json.load(f)
                DisplayAllProject(projectManager , AllProjects , False , username)
            else:
                print('There are no projects yet.')
            time.sleep(3)
            break

        elif choice == '4':
            show_title('[bold deep_sky_blue3]Managing Projects')
            
            if os.path.exists(AllprojectFile):
                with open(AllprojectFile , 'r') as f:
                    AllProjects = json.load(f)
                DisplayAllProject(projectManager , AllProjects , True , username)
            else:
                print('There are no projects yet.')
            time.sleep(3)
            break
            
>>>>>>> ca95177 (Update Everything)
        elif choice == '5':
            return
        elif choice == '6':
            exit(1)
        else:
<<<<<<< HEAD
            choice = input("Please enter a valid number: ")
=======
            choice = get_choice("Please enter a valid number: ")
>>>>>>> ca95177 (Update Everything)
