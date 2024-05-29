import json 
from pathlib import Path  
import uuid
from datetime import datetime,timedelta
from enum import Enum
import sys
from rich.console import Console
from rich.table import Table

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
        super().__init__(f"{name} does not exist.")



class Project:
    def __init__(self , title , projectId , leader):
        self.title = title
        self.id = projectId
        self.leader = leader
        self.tasks = []
        self.members = []
    

    def ToDict(self):
        return{
            'title' : self.title ,
            'id' : self.id,
            'leader' : self.leader,
            'tasks' : self.tasks,
            'members' : self.members
        }
    
    @staticmethod
    def FromDict(data):
        project =  Project(data['title'] , data['id'] , data['leader'])
        project.tasks = data.get('tasks' , [])
        project.members = data.get('members' , [])
        return project
      
        

class ProjectManager(Project): #creat , find , load , add projects.be tore koli baraye modiriate projects
    def __init__(self):
        super().__init__(title = '' , projectId = '' , leader = '')
        self.projects = []

    def findId(self, projectId):
        idsData = Path('data/projectIds.json')
        if idsData.stat().st_size > 0:
            with open(idsData, 'r') as inputFile:
                ids = json.load(inputFile)
                for id in ids:
                    if projectId == id:
                        return False
                return True
        return True


    def AddProject(self , title , projectId , leader):
        try:
            if self.findId(projectId):
                project = Project(title , projectId , leader)
                self.SaveProject(project)
                self.AddMemmber(projectId , title , leader , leader)
                print(f"Project '{title}' created successfully with Id {projectId} .")
                return True
            else:
                raise ValueError(projectId)
        except Exception as e:
            print(f"Error adding project: {e}")
        

    def LoadProjects(self , projectId):
        try:
            datafile = Path('data') / f'project_{projectId}.json'
            dataFile = Path('data') / f'project.json'
            with open(datafile,'r')as f:
                projectData = json.load(f)
                self.projects = [Project.FromDict(project) for project in projectData]
                return self.projects
        except(FileNotFoundError,json.JSONDecodeError) as e:
            print(f"Error loading project: {e}")
            return None 
        

    def LoadAllProjects(self):
        projects = []
        projectFiles = Path('data').glob('project_*.json')
        for projectFile in projectFiles:
            with open(projectFile , 'r') as f:
                projectData = json.load(f)
                project = Project.FromDict(projectData)
                projects.append(project)
                return projects
        
    def SaveProject(self , project):
        try:
            AllprojectFile = Path('data') / f'project.json'
            datafile = Path('data') / f'project_{project.id}.json'
            idData = Path('data/projectIds.json')

            with open(datafile,'w') as f:
                json.dump([project.ToDict()], f, indent=4)   

            project_list = []
            with open(AllprojectFile, 'r') as f:
                project_list = json.load(f)
            DictProject = project.ToDict()
            project_list.append(DictProject)
            with open(AllprojectFile,'w') as f:
                json.dump(project_list, f, indent=4)
                
            with open(idData, 'r') as idFile:
                ids = json.load(idFile)
                if not(project.id in ids):
                    ids.append(project.id)
                with open(idData, 'w') as id: 
                    json.dump(ids , id)
        except IOError as e:
            print(f"Error saving project : {e}")     


        
    def CreateProject(self):
        try:
            title = input("Enter project title: ")
            leader = input("Enter your username: ")
            while True:
                projectId = input("Enter project ID: ")
                while not projectId.isdigit():
                    print("Sorry.You can just use number for ID.")
                    projectId = input("Enter project ID: ")
                    break
                if(self.AddProject(title , projectId , leader)):
                    break
        except Exception as e:
            print(f"Error creating project: {e}")


    def FindProject(self , projectId , username):
        try:
            idsData = Path('data/projectIds.json')
            AllprojectFile = Path('data') / f'project.json'
            with open(AllprojectFile , 'r') as f:
                AllProjects = json.load(f)
            if idsData.stat().st_size > 0:
                with open(idsData, 'r') as inputFile:
                    ids = json.load(inputFile)
                if projectId in ids:
                    position = ids.index(projectId)
                    i = 0
                    if len(AllProjects) > 0:
                        for i in AllProjects[position]["members"]:
                            if username in AllProjects[position]["members"][i]:
                                print("This project is found.")
                    return projectId
                else:
                    return False
            else:
                print("You have not any project yet!")
                return False
        except Exception as e:
            print(f"Error finding project: {e}")
        
        

    def AddMemmber(self ,projectId , projectTitle , username , requester):
        try:
            idsData = Path('data/projectIds.json')
            AllprojectFile = Path('data') / f'project.json'
            with open(AllprojectFile , 'r') as f:
                AllProjects = json.load(f)
            if idsData.stat().st_size > 0:
                with open(idsData, 'r') as inputFile:
                    ids = json.load(inputFile)
                if projectId in ids:
                    position = ids.index(projectId)
            project = self.FindProject(projectId , username)
            if project:
                if requester == AllProjects[position]["leader"]:
                    if len(AllProjects) > 0:
                        if username not in AllProjects[position]["members"]:
                            AllProjects[position]["members"].append(username)
                            self.SaveProject(AllProjects[position])
                            print(f"User {username} added to '{projectTitle}'.")
                        else:
                            print(f"User {username} is already a member of the project '{projectTitle}'.")
                else:
                    raise PremissionError()
        except ProjectError as e:
            print(f"Error adding memeber: {e}")



    def RemoveMember(self , projectId , projectTitle , username , requester):
        try:
            idsData = Path('data/projectIds.json')
            AllprojectFile = Path('data') / f'project.json'
            with open(AllprojectFile , 'r') as f:
                AllProjects = json.load(f)
            if idsData.stat().st_size > 0:
                with open(idsData, 'r') as inputFile:
                    ids = json.load(inputFile)
                if projectId in ids:
                    position = ids.index(projectId)
            project = self.FindProject(projectId , username)
            if project:
                if requester == AllProjects[position]["leader"]:
                    if len(AllProjects) > 0:
                        if username in AllProjects[position]["members"]:
                            index = AllProjects[position]["members"].index(username)
                            AllProjects[position]["members"].pop(index)
                            self.SaveProject(AllProjects[position])
                            print(f"User {username} removed from '{projectTitle}'.")
                        else:
                            print(f"User {username} is not a member of the project '{projectTitle}'.")
                else:
                    raise PremissionError()
        except ProjectError as e:
            print(f"Error removing memeber: {e}")


    def DeletProject(self , projectId , projectTitle , requester):
        try:
            idsData = Path('data/projectIds.json')
            AllprojectFile = Path('data') / f'project.json'
            with open(AllprojectFile , 'r') as f:
                AllProjects = json.load(f)
            if idsData.stat().st_size > 0:
                with open(idsData, 'r') as inputFile:
                    ids = json.load(inputFile)
                if projectId in ids:
                    position = ids.index(projectId)
            project = self.FindProject(projectId , requester)
            if project:
                if requester == AllProjects[position]["leader"]:
                    AllProjects.pop(position)
                    ids.pop(position)
                    dataFile = Path('data')/f'project_{projectId}.json'
                    AllprojectFile = Path('data') / f'project.json'
                    idsData = Path('data/projectIds.json')
                    dataFile.unlink()
                    print(f"The project '{projectTitle}' deleted successfully.")
                else:
                    raise PremissionError()
        except Exception as e:
            print(f"Error deleting project: {e}")


    def LeaderProjects(self , username):
        try:
            AllprojectFile = Path('data') / f'project.json'
            with open(AllprojectFile , 'r') as f:
                AllProjects = json.load(f)
            it = 0
            if len(AllProjects) > 0:
                temp = 0
                for it in range(len(AllProjects)):
                    if AllProjects[it]["leader"] == username:
                        print(AllProjects[it]["title"])
                        temp += 1
                if temp == 0:
                    print("You are not a leader of any project.")
            else:
                print("There is no project yet")
        except Exception as e:
            print(f"Error Showing project member: {e}")


    def MemeberProject(self , username):
        try:
            AllprojectFile = Path('data') / f'project.json'
            with open(AllprojectFile , 'r') as f:
                AllProjects = json.load(f)
            it = 0
            if len(AllProjects) > 0:
                for it in range(len(AllProjects)):
                    i = 0
                    temp = 0
                    for i in AllProjects[it]["members"]:
                        if AllProjects[it]["members"][i] == username:
                            print(AllProjects[it]["title"])
                            temp += 1
                if temp == 0:
                    print("You are not a member of any project.")
        except Exception as e:
            print(f"Error Showing project member: {e}")

    def DisplayProject(self , project):
        print(f"Project ID: {project.id}")
        print(f"Title: {project.title}")
        print(f"Leader: {project.leader}")
        print(f"Members: {''.join.project.members}")
        print(f"Tasks: {project.tasks}")





############





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
    def __init__(self , title = '' , description = '' , priority = Priority.LOW , status = Status.BACKLOG):
        self.id = str(uuid.uuid4())
        self.title = title
        self.description = description
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
            'description' : self.description,
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
        return Task(data['title'] , data['description'] , data['assignees'] , data['priority'] , data['status'])
    


class TaskManager(Task): 
    def __init__(self):
        self.tasks = []

    
    def LoadTasks(self):
        try:
            datafile = Path('taskData/task.json')
            with open(datafile,'r')as f:
                taskData = json.load(f)
                return [Task(task) for task in taskData]
        except(FileNotFoundError,json.JSONDecodeError) as e:
            print(f"Error loading task: {e}")
            return [] 
        
    def SaveTask(self , task):
        try:
            datafile = Path('taskData/task.json')
            with open(datafile,'w') as f:
                json.dump([task.ToDict() for task in self.tasks], f, indent=4)   
        except IOError as e:
            print(f"Error saving task : {e}")  

    def AddTask(self, title ,discription ,assignees , priority , status):
        task = Task(title ,discription , Priority[priority] , Status[status])
        task.assignees = assignees
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
        try:
            task = self.FindTask(TaskId)
            if username in task.assignees:
                for key , value in kwargs.items():
                    if key == 'title':
                        task.title = value
                    elif key == 'description':
                        task.description = value
                    elif key == 'priority':
                        task.priority = Priority[value]
                    elif key == 'status':
                        task.status = Status[value]
                    elif key == 'endTime':
                        task.endTime = datetime.fromisoformat(value)
                    task.history.append((datetime.now().isoformat() , kwargs))
                    self.SaveTask()
                    print(f"Task '{task.title}' updated successfully.")
                    if hasattr(task , key):
                        oldValue = getattr(task , key)
                        setattr(task , key , value)
                        if key in ['priority' , 'status' , 'assignees']:
                            task.history.append({'user': username , 'time': datetime.now().isoformat() , 'change': f"{key} changed from {oldValue} to {value}."})
                            self.SaveTask()
                            print("Task updated successfully.")
        except NotFoundError as e:
            print(e)
    



    def DisplayTasksByStatus(self, projectId):
        try:
            project = ProjectManager.FindProject(projectId)
            console = Console()
            table = Table(title=f"Tasks for Project {project.title}")

            # Add columns for each status
            for status in Status:
                table.add_column(status.value)

            # Collect tasks by status
            TasksByStatus = {status: [] for status in Status}
            for task in project.tasks:
                TasksByStatus[task.status].append(task)

            # Determine the maximum number of tasks in any status for row alignment
            max_tasks = max(len(tasks) for tasks in TasksByStatus.values())

            # Add rows to the table
            for i in range(max_tasks):
                row = []
                for status in Status:
                    if i < len(TasksByStatus[status]):
                        task = TasksByStatus[status][i]
                        row.append(task.title)
                    else:
                        row.append("")
                table.add_row(*row)

            console.print(table)

            taskId = input("Enter the ID of the task you want to view or edit: ")
            task = self.find_task(taskId)
            self.DisplayTaskDetails(task)

        except ProjectError as e:
            print(f"Error displaying tasks: {e}")

    def DisplayTaskDetails(self, task):
        console = Console()
        console.print(f"ID: {task.id}")
        console.print(f"Title: {task.title}")
        console.print(f"Description: {task.description}")
        console.print(f"Priority: {task.priority.value}")
        console.print(f"Status: {task.status.value}")
        console.print(f"Start Time: {task.startTime}")
        console.print(f"End Time: {task.endTime}")
        console.print(f"Assignees: {', '.join(task.assignees)}")

        if input("Do you want to edit this task? (y/n): ").lower() == 'y':
            updates = {}
            title = input("Enter new title (leave blank to keep current): ")
            if title:
                updates['title'] = title
            description = input("Enter new description (leave blank to keep current): ")
            if description:
                updates['description'] = description
            priority = input(f"Enter new priority ({', '.join(p.name for p in Priority)}) (leave blank to keep current): ")
            if priority:
                updates['priority'] = priority
            status = input(f"Enter new status ({', '.join(s.name for s in Status)}) (leave blank to keep current): ")
            if status:
                updates['status'] = status
            end_time = input("Enter new end time (YYYY-MM-DD) (leave blank to keep current): ")
            if end_time:
                updates['endTime'] = end_time

            self.UpdateTask(task.id, task.assignees[0], **updates)
        


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

    


def DisplayProjectTask(tasks):
    if len(tasks) == 0:
        print("There are no tasks in this project.")
        return
    table = Table(title="ProjectTaska")
    table.add_column("ID" , style="bold")
    table.add_column("Title",style="bold")
    table.add_column("Description")
    table.add_column("Priority")
    table.add_column("Status")
    for task in tasks:
        table.add_row(task.id , task.title , task.discription , task.priority.value , task.status.value)
    console = Console()
    console.print(table)



def DisplayAllProject(projects):
    if len(projects) == 0:
        print("There are no projects.")
        return
    temp = 0
    it = 0
    for it in range(len(projects)):
        temp += 1
        print(f"{it}.{projects[it]["title"]} / ID: {projects[it]["id"]})")
    choice = input("Which one you choose?")
    if int(choice) > int(temp) and int(choice) <= 0:
        print("Invalid choice.Pleas try again.") 
    project = projects[choice - 1]
    DisplayProjectTask(project["tasks"])




def ProjectMenu(project , username):
    while True:
        print("[1] View members")##member in each project
        print("[2] View Tasks")##all of task in each project
        print("[3] View Leader")## show username of leader of each project
        print("[4] View tasks assigned to a member")##all task in each project that assigned to a member
        if username == project.leader:
            print("[5] Add a member to the project")
            print("[6] Remove a member from the project")
            print("[7] Deleting the project")
            print("[8] Delet member from a task")
            print("[9] Add task to project")
            print("[10] Back to main menu")
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
            project.RemoveMember(project.id , project.title , Adduser , username)
        elif choice == '7' and username == project.leader:
            project.DeletProject(project.id , project.title , username)
        elif choice == '8' and username == project.leader:
            projectId = input("Enter projectId: ")
            task = Task()
            task.RemoveAssignee(username , username , projectId)
        elif choice == '9' and username == project.leader:
            title = input("Enter task title:")
            description = input("Enter task descroption")
            assignees = input("Enter assignees (comma-separated): ").split(",")
            priority = input(f"Enter task priority ({','.join(p.name for p in Priority)}): ")
            status = input(f"Enter task status ({','.join(s.name for s in Status)}): ")
            taskManager = TaskManager()
            taskManager.DisplayTasksByStatus(projectId)
        elif choice == '10' and username == project.leader:
            break
        else:
            print("Invalid choice.Please try again.")

def Menu():
    print("[1] Creat a new project")
    print("[2] Projects that you a member of.")
    print("[3] Projects that you a leader of.")
    print("[4] View all projects.")
    print("[5] Exit")
    choice = input("Enter your choice: ")
    return choice  

def main():
    username = input("Enter your username:")
    while True:
        projectManager = ProjectManager()
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
            idsData = Path('data/projectIds.json')
            AllprojectFile = Path('data') / f'project.json'
            with open(AllprojectFile , 'r') as f:
                AllProjects = json.load(f)
            DisplayAllProject(AllProjects)
        elif choice == '5':
            print("Exiting...")
            sys.exit()
        else:
            print("Invalid choice.Please try again.")


if __name__ == "__main__":
    main()