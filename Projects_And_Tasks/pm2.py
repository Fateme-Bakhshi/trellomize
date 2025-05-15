from .task import TaskManager
from .task import TableTask
from .project import ProjectManager
import shutil, json #for save file
from pathlib import Path  #for save file
import os, logging, time, sys
from rich.console import Console
from Users.user import UserManager

logging.basicConfig(filename="logFile/actions.log", format='%(asctime)s - %(message)s', filemode='a', level=logging.DEBUG)

def clear_screen():
    os.system('cls')
    

def show_title(title):
    clear_screen()
    console = Console()
    print('\n')
    console.rule(title, style="bold white")
    time.sleep(1)

def get_choice(text):
    columns = shutil.get_terminal_size().columns
    spaces = (columns - len(text)) // 2
    print(' ' * spaces + text, end="")
    choice = input()
    return choice

def back():
    choice = input('\n[0]Back\n')
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




def ProjectMenu(projectManager , project , username):
    """Menu for project and tasks

    Args:
        projectManager (_type_): _description_
        project (_type_): _description_
        username (_type_): _description_
    """
    while True:
        time.sleep(5)
        clear_screen()
        print("\n")
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
                    for j in range(len(project["tasks"][i]["comments"])):
                        print(f"{int(j) + 1}.")
                        print(f'  User : {project["tasks"][i]["comments"][j]["user"]}')
                        print(f'  Description : {project["tasks"][i]["comments"][j]["description"]}')
        elif choice == '3':
            print(f'Leader: {project["leader"]}')

        elif choice == '4':
            if len(project["tasks"]) == 0:
                print("There are no tasks yet.")
            else:
                member = input("Enter username of member: ")
                i = 0
                temp = 0
                for i in range(len(project["tasks"])):
                    if member in project["tasks"][i]["assigners"]:
                        temp += 1
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

        elif choice == '8' and username == project["leader"]:
            taskManager = TaskManager()
            taskManager.CreatTask(project["id"])

        elif choice == '9' and username == project["leader"]:
            return
        else:
            print("Invalid choice.Please try again.")


def Main(choice, username):
    projectManager = ProjectManager()
    AllprojectFile = Path('Projects_Data/project.json')
    print("\n")
    while True:
        if choice == '1':
            clear_screen()
            show_title('[bold deep_sky_blue1]Member Projects')
            projectManager.MemeberProject(username)
            if back():
                break
        
        elif choice == '2':
            clear_screen()
            show_title('[bold deep_sky_blue1]Leader Projects')
            projectManager.LeaderProjects(username)
            if back():
                break
        
        elif choice == '3':
            clear_screen()
            show_title('[bold deep_sky_blue1]Managing Tasks')
            
            if os.path.exists(AllprojectFile):
                with open(AllprojectFile , 'r') as f:
                    AllProjects = json.load(f)
                DisplayAllProject(projectManager , AllProjects , False , username)
            else:
                print('There are no projects yet.')
                
            if back():
                break

        elif choice == '4':
            clear_screen()
            show_title('[bold deep_sky_blue1]Managing Projects')
            
            if os.path.exists(AllprojectFile):
                with open(AllprojectFile , 'r') as f:
                    AllProjects = json.load(f)
                DisplayAllProject(projectManager , AllProjects , True , username)
            else:
                print('There are no projects yet.')
                
            if back():
                break
            
        elif choice == '5':
            return
        elif choice == '6':
            exit(1)
        else:
            choice = get_choice("Please enter a valid number: ")
