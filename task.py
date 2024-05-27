import uuid
import json
from pathlib import Path
from datetime import datetime,timedelta
from enum import Enum
from project import ProjectManager
from tabulate import tabulate
import sys

class ProjectError(Exception):
    pass

class PremissionError(ProjectError):
    def __init__(self):
        super().__init__("You are not leader.")

class ValueError(ProjectError):
    def __init__(self , number):
        super().__init__(f"This {number} is not valid.")

class NotFoundError(ProjectError):
    def __init__(self, name):
        super().__init__(f"{name} is not already exist.")



class Priority(Enum):
    CRITICAL = 'CRITICAL'
    HIGH = 'HIGH'
    MEDIUM = 'MEDIUM'
    LOW = 'LOW'


class Status(Enum):
        BACKLOG = 'BACKLOG'
        TODO = 'TODO'
        DOING = 'DOING'
        DONE = 'DONE'
        ARCHIVED = 'ARCHIVED'


class Task:
    def __init__(self , title = '' , discription = '' , priority = Priority.LOW , status = Status.BACKLOG):
        self.id = str(uuid.uuid4())
        self.title = title
        self.discription = discription
        self.startTime = datetime.now()
        self.endTime = self.startTime + timedelta(days=1)
        self.assignees = []
        self.priority = priority
        self.status = status
        self.history = []
        self.comments = []
        self.members = []


    def ToDict(self):
        return{
            'id' : self.id,
            'title' : self.title,
            'discription' : self.discription,
            'startTime' : self.startTime.isoformat(),
            'endTime' : self.endTime.isoformat(),
            'assignees' : self.assignees,
            'priority' : self.priority.value,
            'status' : self.status.value,
            'history' : self.history,
            'comments' : self.comments,
            'members' : self.members
        }
    
    def FromDict(data):
        return Task(data['title'] , data['discription'] , data['assignees'] , data['priority'] , data['status'])
    


class TaskManager(Task): 
    def __init__(self):
        self.tasks = self.LoadTasks()

    
    def LoadTasks(self):
        try:
            datafile = Path('taskData\\task.json')
            with open(datafile,'r')as f:
                taskData = json.load(f)
                return [Task(task) for task in taskData]
        except(FileNotFoundError,json.JSONDecodeError) as e:
            print(f"Error loading task: {e}")
            return [] 
        
    def SaveTask(self , task):
        try:
            datafile = Path('taskData\\task.json')
            with open(datafile,'w') as f:
                json.dump([task.ToDict()], f, indent=4)   
        except IOError as e:
            print(f"Error saving task : {e}")  

    def AddTask(self, title ,discription ,assignees , priority , status):
        task = Task(title ,discription ,assignees , priority , status)
        self.tasks.append(task)
        self.SaveTask()


    def FindTask(self , taskId):
        try:
            for task in self.tasks:
                if task.id == taskId:
                    return task
        except NotFoundError(taskId) as e:
            print(f"{e}")

    def AddMemmber(self ,taskId ,username , requester , projectId):
        try:
            task = self.FindTask(taskId)
            if task:
                if requester == projectId.leader:
                    if username not in task.members:
                        task.members.append(username)
                        self.SaveTask()
                        print(f"User {username} added to '{taskId}'.")
                    else:
                        print(f"User {username} is already a member of '{taskId}'.")
                else:
                    raise PremissionError()
            else:
                raise NotFoundError(taskId)
        except ProjectError as e:
            print(f"Error adding memeber: {e}")


    def UpdateTask(self , TaskId , username , **kwargs):
        task = self.FindTask(TaskId)
        if task:
            for key , value in kwargs.items():
                if hasattr(task , key):
                    oldValue = getattr(task , key)
                    setattr(task , key , value)
                    if key in ['priority' , 'status' , 'assignees']:
                        task.history.append({'user': username , 'time': datetime.now().isoformat() , 'change': f"{key} changed from {oldValue} to {value}."})
                        self.SaveTask()
                        print("Update task successfully.")
                        return task
        else:
            raise NotFoundError(TaskId)

        


    def AddComment(self , username , content):
        self.comments.append({'user' : username , 'time': datetime.now().isoformat , 'content' : content})

    def AddCommentToTask(self , taskId , username , content):
        task = self.FindTask(taskId)
        if task:
            task.AddComment(username , content)
            self.SaveTask()
            print("Add comment successfully.")
            return task
        else:
            raise NotFoundError(taskId)

        
    def AssignTask(self , taskId , assignees , leader , requester , projectId):
        task = self.FindTask(taskId)
        if not task:
            raise NotFoundError(taskId)
        if requester != leader:
            raise PremissionError()
        if user not in projectId.members:
            raise NotFoundError(user)
        for user in assignees:
            if user not in task.assignees:
                task.assignees.append(user)
                task.history.append({'user' : leader , 'time': datetime.now().isoformat , 'change': f"Assigned  to {user}"})
                self.SaveTask()
                return task
            
    def RemoveAssignee(self , assignee , username , projectId):
        if username != projectId.leader:
            raise PremissionError()
        if assignee not in self.assignees:
            raise NotFoundError(assignee)
        self.assignees.remove(assignee)
        
    
    def CreatTask(self):
        try:
            title = input("Enter task title: ")
            while True:
                taskId = Task.id
                try:
                    self.IsUnicId(taskId)
                    task = Task(title , taskId)
                    self.projects.append(task)
                    self.SaveTask()
                    print(f"Task '{title}' created successfully with Id {task.id} .")
                    break
                except ValueError as e:
                    print(e)
        except Exception as e:
            print(f"Error creating task: {e}")
    


def Findproject(self , projectt):
    userid = input("Enter your username")
    projects = projectt.MemeberProject(userid)
    if projects == False:
        return
    for index , project in enumerate(projects,1):
        print(f"{index}.{project.title} (ID: {project.id})")
        projectChoice = int(input("Select a project by number: "))
        selectedProject = projects[projectChoice - 1]
        projectt.DisplayeProject(selectedProject)
        ProjectMenu()

    

def Menu():
    print("[1] Creat a new project")
    print("[2] Manage existing projects")
    print("[3] Exit")
    choice = input("Enter your choice: ")
    return choice
    

def UserProjectMenu(project , username):
    while True:
        print("[1] Projects that you a member of.")
        print("[2] Projects that you a leader of.")
        choice = input("Enter your choice: ")
        if choice == 1:
            project = ProjectManager()
            project.LeaderProjects(username)
        elif choice == 2:
            project = ProjectManager()
            project.MemeberProject(username)
        else:
            print("Invalid choice.Please try again.")
        

def ProjectMenu(project , username):
    while True:
        print("[1] View members")
        print("[2] View Tasks")
        print("[3] View Leader")
        print("[4] View tasks assigned to a member")
        if username == project.leader:
            print("[5] Add a member to the project")
            print("[6] Remove a member from the project")
            print("[7] Deleting the project")
            print("[8] Delet member from a task")
            print("[9] Back to main menu")
        else:
            print("[5] Back to main menu")
        choice = input("Enter your choice")
        if choice == '1':
            print(f"Members: {''.join.project.members}")
        elif choice == '2':
            print(f"Tasks: {project.tasks}")
        elif choice == '3':
            print(f"Leader: {project.leader}")
        elif choice == '4':
            member = input("Enter member username: ")
            tasks = [task for task in project.tasks if member in task.get('assignees' , [])]
            print(f"Tasks assigned to {member}: {tasks}")
        elif username != project.leader and choice == '5':
            break
        elif choice == '5' and username == project.leader:
            Adduser = input("Enter the ID you want to add.")
            project.AddMember(project.id , project.title , Adduser , username)
        elif choice == '6' and username == project.leader:
            Adduser = input("Enter the ID you want to remove.")
            project.DeletProject(project.id , project.title , Adduser , username)
        ##elif choice == '7' and username == project.leader:
        elif choice == '8' and username == project.leader:
            projectId = input("Enter projectId: ")
            task = Task()
            task.RemoveAssignee(username , username , projectId)
        elif choice == '9' and username == project.leader:
            break
        else:
            print("Invalid choice.Please try again.")
    

def main():
    while True:
        print("\n")
        choice = Menu()
        if choice == '1':
            print("Creating a new project....")
            project = ProjectManager()
            project.CreateProject()
        elif choice == '2':
            username = input("Enter tour username:")
            projectId = input("Enter projectID:")
            projectt = ProjectManager()
            project = projectt.FindProject(projectId)
            UserProjectMenu(project , username)
        elif choice == '3':
            print("Exiting...")
            sys.exit()
        else:
            print("Invalid choice.Please try again.")


if __name__ == "__main__":
    main()