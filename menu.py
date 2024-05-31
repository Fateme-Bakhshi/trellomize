import sys #for exit
from task import TaskManager
from task import TableTask
from project import ProjectManager
import json #for save file
from pathlib import Path  #for save file


def DisplayAllProject(projectManager , projects , Isbool , username):
    """Show all proejcts

    Args:
        projectManager (_type_): _object or dict of project_
        projects (_type_): _projects_
        Isbool (_type_): _bool_
        username (_type_): _username_
    """
    try:
        if len(projects) == 0:
            print("There are no projects.")
            return
        temp = 0
        it = 0
        for it in range(len(projects)):
            temp += 1
            print(f"({int(it) + 1}.{projects[it]["title"]} / ID: {projects[it]["id"]})")
        choice = input("Which one you choose? ")
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
        choice = input("Enter your choice: ")
        if choice == '1':
            if len(project["members"]) == 0:
                print("This project doesn't have any member")
            else:
                i = 0
                print("Members:")
                for i in range(len(project["members"])):
                    print(f"{int(i + 1)}. {project["members"][i]}")

        elif choice == '2':
            if len(project["tasks"]) == 0:
                print("There is no task yet")
            else:
                i = 0
                print("Tasks:")
                for i in range(len(project["tasks"])):
                    print(f"{int(i + 1)}]")
                    print(f" Title: {project["tasks"][i]["title"]}")
                    print(f" ID: {project["tasks"][i]["id"]}")
                    print(f" Description: {project["tasks"][i]["description"]}")
                    print(f" Assignees: {','.join(project["tasks"][i]["assignees"])}")
                    print(f" Start Time: {project["tasks"][i]["startTime"]}")
                    print(f" End Time: {project["tasks"][i]["endTime"]}")
                    print(f" Priority: {project["tasks"][i]["priority"]}")
                    print(f" Status: {project["tasks"][i]["status"]}")
                    print(" History:")
                    for it in range(len(project["tasks"][i]["history"])):
                        print(f"{int(it) + 1}.")
                        print(f"  User : {project["tasks"][i]["history"][it]["user"]}")
                        print(f"  Description : {project["tasks"][i]["history"][it]["action"]}")
                    print(" Comments:")
                    for j in range(len(project["tasks"][i]["comments"])):
                        print(f"{int(j) + 1}.")
                        print(f"  User : {project["tasks"][i]["comments"][j]["user"]}")
                        print(f"  Description : {project["tasks"][i]["comments"][j]["description"]}")
        elif choice == '3':
            print(f"Leader: {project["leader"]}")

        elif choice == '4':
            if len(project["tasks"]) == 0:
                print("There is no task yet")
            else:
                member = input("Enter username of member: ")
                i = 0
                temp = 0
                for i in range(len(project["tasks"])):
                    if member in project["tasks"][i]["assignees"]:
                        temp += 1
                        print(f"{member} assigned to this task {project["tasks"][i]["title"]}")
                if temp == 0:
                    print(f"{username} is assigned to no tasks")

        elif username != project["leader"] and choice == '5':
            return

        elif choice == '5' and username == project["leader"]:
            Adduser = input("Enter the ID you want to add: ")
            projectManager.AddMember(project["id"] , project["title"] , Adduser , username)
        
        elif choice == '6' and username == project["leader"]:
            removeuser = input("Enter the ID you want to remove: ")
            projectManager.RemoveMember(project["id"] , project["title"] , removeuser , username)

        elif choice == '7' and username == project["leader"]:
            project.DeletProject(project["id"] , project["title"] , username)

        elif choice == '8' and username == project["leader"]:
            taskManager = TaskManager()
            taskManager.CreatTask(project["id"])

        elif choice == '9' and username == project["leader"]:
            return
        else:
            print("Invalid choice.Please try again.")

def Menu():
    """Menu for projects

    Returns:
        _type_: _description_
    """
    print("[1] Creat a new project")
    print("[2] Projects that you a member of.")
    print("[3] Projects that you a leader of.")
    print("[4] View all projects and change tasks.")
    print("[5] View all projects and change the project.")
    print("[6] Exit")
    choice = input("Enter your choice: ")
    return choice  

def main():
    username = input("Enter your username:")
    while True:
        projectManager = ProjectManager()
        idsData = Path('data/projectIds.json')
        AllprojectFile = Path('data') / f'project.json'
        print("\n")
        choice = Menu()
        if choice == '1':
            print("Creating a new project....")
            projectManager.CreateProject()

        elif choice == '2':
            projectManager.MemeberProject(username)

        elif choice == '3':
            projectManager.LeaderProjects(username)

        elif choice == '4':
            print("Project List:")
            with open(AllprojectFile , 'r') as f:
                AllProjects = json.load(f)
            DisplayAllProject(projectManager , AllProjects , False , username)

        elif choice == '5':
            with open(AllprojectFile , 'r') as f:
                AllProjects = json.load(f)
            DisplayAllProject(projectManager , AllProjects , True , username)

        elif choice == '6':
            print("Exiting...")
            sys.exit()
        else:
            print("Invalid choice.Please try again.")
