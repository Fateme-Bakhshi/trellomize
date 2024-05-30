import json #for save file
from pathlib import Path  #for save file
import uuid # for unic id
from datetime import datetime,timedelta #for time
from enum import Enum #for Enum Class
import sys #for exit
from rich.console import Console #for table
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
    
      
        

class ProjectManager(Project): 
    def __init__(self):
        super().__init__(title = '' , projectId = '' , leader = '')


    def findId(self, projectId):
        """
        Args:
            projectId (_type_): _id of project_

        Returns:
            _type_: _description_
        """
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
        """
        Args:
            title (_type_): _title of project_
            projectId (_type_): _id of project_
            leader (_type_): _someone who creat project_

        Raises:
            ValueError: _Error of value_

        Returns:
            _type_: _description_
        """
        try:
            if self.findId(projectId):
                project = Project(title , projectId , leader)
                project = project.ToDict()
                project["leader"] = leader
                project["members"].append(leader)
                self.SaveProject(project)
                print(f"Project '{title}' created successfully with Id {projectId} .")
                return True
            else:
                raise ValueError(projectId)
        except Exception as e:
            print(f"Error adding project: {e}")

        
    def SaveProject(self , project):
        """_save project to jsonFile_

        Args:
            project (_type_): _dict or object_
        """
        try:
            if not isinstance(project , dict):
                project = project.ToDict()
            AllprojectFile = Path('data') / f'project.json'
            datafile = Path('data') / f'project_{project["id"]}.json'
            idData = Path('data/projectIds.json')

            with open(datafile,'w') as f:
                json.dump(project, f, indent=4)   
            project_list = []
            with open(AllprojectFile, 'r') as f:
                project_list = json.load(f)
            project_list.append(project)
            with open(AllprojectFile,'w') as f:
                json.dump(project_list, f, indent=4)
            with open(idData, 'r') as idFile:
                ids = json.load(idFile)
                if not(project["id"] in ids):
                    ids.append(project["id"])
                with open(idData, 'w') as id: 
                    json.dump(ids , id)
        except IOError as e:
            print(f"Error saving project : {e}")     


        
    def CreateProject(self):
        """
            creat project
        """
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
        """

        Args:
            projectId (_type_): _id of project_
            username (_type_): _user_

        Returns:
            _type_: _description_
        """
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
                        for i in range(len(AllProjects[position]["members"])):
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
        
        
    
    def AddMember(self ,projectId , projectTitle , username , requester):
        """
        Args:
            projectId (_type_): _id of project_
            projectTitle (_type_): _title of project_
            username (_type_): _user_
            requester (_type_): _requester for add member_

        Raises:
            PremissionError: _description_
        """
        try:
            idsData = Path('data/projectIds.json')
            AllprojectFile = Path('data') / f'project.json'
            datafile = Path('data') / f'project_{projectId}.json'
            with open(AllprojectFile , 'r') as f:
                AllProjects = json.load(f)
            if idsData.stat().st_size > 0:
                with open(idsData, 'r') as inputFile:
                    ids = json.load(inputFile)
                if projectId in ids:
                    position = ids.index(projectId)
            with open(datafile , 'r') as f:
                project1 = json.load(f)
            if requester == AllProjects[position]["leader"]:
                if len(AllProjects) > 0:
                    if username not in AllProjects[position]["members"]:
                        AllProjects[position]["members"].append(username)
                        project1["members"].append(username)
                        with open(AllprojectFile , 'w') as f:
                            json.dump(AllProjects , f ,indent=4)
                        with open(datafile , 'w') as f:
                            json.dump(project1 , f , indent=4)
                        print(f"User {username} added to '{projectTitle}'.")
                    else:
                        print(f"User {username} is already a member of the project '{projectTitle}'.")
            else:
                raise PremissionError()
        except ProjectError as e:
            print(f"Error adding memeber: {e}")


    def RemoveMember(self , projectId , projectTitle , username , requester):
        """
        Args:
            projectId (_type_): _id of project_
            projectTitle (_type_): _title of project_
            username (_type_): _username_
            requester (_type_): _requester for remove member_

        Raises:
            PremissionError: _description_
        """
        try:
            idsData = Path('data/projectIds.json')
            AllprojectFile = Path('data') / f'project.json'
            datafile = Path('data') / f'project_{projectId}.json'
            with open(AllprojectFile , 'r') as f:
                AllProjects = json.load(f)
            if idsData.stat().st_size > 0:
                with open(idsData, 'r') as inputFile:
                    ids = json.load(inputFile)
                if projectId in ids:
                    position = ids.index(projectId)
            with open(datafile , 'r') as f:
                project1 = json.load(f)
            if requester == AllProjects[position]["leader"]:
                if username == AllProjects[position]["leader"]:
                    print("Sorry.You are leader.You can not remove yourself.")
                else:
                    if len(AllProjects) > 0:
                        i = 0
                        for i in range(len(AllProjects[position]["members"])):
                            if username == AllProjects[position]["members"][i]:
                                AllProjects[position]["members"].pop(i)
                                project1["members"].pop(i)
                                with open(AllprojectFile , 'w') as f:
                                    json.dump(AllProjects , f ,indent=4)
                                with open(datafile , 'w') as f:
                                    json.dump(project1 , f , indent=4)
                                print(f"User {username} removed from '{projectTitle}'.")
                            else:
                                print(f"User {username} is not a member of the project '{projectTitle}'.")
            else:
                raise PremissionError()
        except ProjectError as e:
            print(f"Error removing memeber: {e}")


    def DeletProject(self , projectId , projectTitle , requester):
        """
        Args:
            projectId (_type_): _id of project_
            projectTitle (_type_): _title of project_
            requester (_type_): _requester for delet project_

        Raises:
            PremissionError: _description_
        """
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
        """_show list of projects that user a leader of those_

        Args:
            username (_type_): _username_
        """
        try:
            AllprojectFile = Path('data') / f'project.json'
            with open(AllprojectFile , 'r') as f:
                AllProjects = json.load(f)
            it = 0
            if len(AllProjects) > 0:
                temp = 0
                for it in range(len(AllProjects)):
                    if username == AllProjects[it]["leader"]:
                        print(f"{AllProjects[it]["title"]} / ID : {AllProjects[it]["id"]}")
                        temp += 1
                if temp == 0:
                    print("You are not a leader of any project.")
            else:
                print("There is no project yet.")
        except Exception as e:
            print(f"Error Showing project member: {e}")


    
    def MemeberProject(self , username):
        """_show list of projects that user just a member of those_

        Args:
            username (_type_): _username_
        """
        try:
            AllprojectFile = Path('data') / f'project.json'
            with open(AllprojectFile , 'r') as f:
                AllProjects = json.load(f)
            it = 0
            if len(AllProjects) > 0:
                for it in range(len(AllProjects)):
                    i = 0
                    temp = 0
                    for i in range(len(AllProjects[it]["members"])):
                        if username == AllProjects[it]["members"][i] and username != AllProjects[it]["leader"]:
                            print(f"{AllProjects[it]["title"]} / ID : {AllProjects[it]["id"]}")
                            temp += 1
                if temp == 0:
                    print("You are not a member of any project.")
        except Exception as e:
            print(f"Error Showing project member: {e}")

    


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
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.title = ""
        self.description = ""
        self.startTime = datetime.now() 
        self.endTime = self.startTime + timedelta(days=1)
        self.assignees = []
        self.priority = "LOW"
        self.status = "BACKLOG"
        self.history = []
        self.comments = []


    def ToDictTask(self):
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
        }
    
    def ToDictComment(self , description , user , time):
        return{
            'description' :  description,
            'user' : user ,
            'time' : time
        }

    def ToDictHistory(self , user , time , action):
        return{
            'user' : user,
            'time' : time,
            'action' : action
        }
    
    


class TaskManager(Task): 
    def __init__(self):
        super().__init__(self)


    def CreatTask(self , projectId):
        """creat new task

        Args:
            projectId (_type_): _id of project_
        """
        try:
            task = TaskManager()
            answer1 = input("Do you want to writ title for task? y/n")
            while True:
                if answer1 == 'y':
                    title = input("Enter title:")
                    task.title = title
                    break
                elif answer1 != 'n':
                    print("Invalid answer.Pleas try again.")
                    input(answer1)
            answer2 = input("Do you want to writ description? y/n")
            while True:
                if answer2 == 'y':
                    description = input("Enter description:")
                    task.description = description
                    break
                elif answer2 != 'n':
                    print("Invalid answer.Pleas try again.")
                    input(answer2)
            taskDict = self.ToDictTask(task)
            AllprojectFile = Path('data') / f'project.json'
            datafile = Path('data') / f'project_{projectId}.json'
            with open(AllprojectFile , 'r') as f:
                AllProjects = json.load(f)
            i = 0
            for i in range(len(AllProjects)):
                if AllProjects[i]["id"] == projectId:
                    if task not in AllProjects[i]["tasks"]:
                        AllProjects[i]["tasks"].append(taskDict)
                        with open(datafile,'r') as f:
                            project = json.load(f)
                        project["tasks"].append(taskDict)
                        print(f"Task '{AllProjects[i]["tasks"]["title"]}' created successfully with Id {AllProjects[i]["tasks"]["id"]} .")
        except Exception as e:
            print(f"Error creating task: {e}")



    def AddMemberToTask(self ,username , requester , projectId):
        """_Assign member to task_

        Args:
            username (_type_): _username_
            requester (_type_): _requester for add_
            projectId (_type_): _project id_

        Raises:
            PremissionError: _description_
        """
        try:
            idsData = Path('data/projectIds.json')
            AllprojectFile = Path('data') / f'project.json'
            datafile = Path('data') / f'project_{projectId}.json'
            with open(datafile,'r') as f:
                project = json.load(f)
            with open(AllprojectFile , 'r') as f:
                AllProjects = json.load(f)
            if idsData.stat().st_size > 0:
                with open(idsData, 'r') as inputFile:
                    ids = json.load(inputFile)
                if projectId in ids:
                    position = ids.index(projectId)
            if requester == AllProjects[position]["leader"]:
                    if len(AllProjects) > 0: 
                        if username not in AllProjects[position]["task"]["assignees"]:
                            AllProjects[position]["task"]["assignees"].append(username)
                            time = datetime.now()
                            action = f"{username} add to the task {AllProjects[position]["task"]["title"]}"
                            historyDict = self.ToDictHistory(requester , time , action)
                            AllProjects[position]["task"]["history"].append(historyDict)
                            project["tasks"]["assignees"].append(username)
                            project["task"]["history"].append(historyDict)
                            with open(AllprojectFile , 'w') as f:
                                json.dump(AllProjects , f ,indent=4)
                            with open(datafile , 'w') as f:
                                json.dump(project , f , indent=4)
                            print(f"User {username} added to '{AllProjects[position]["task"]["title"]}'.")
                        else:
                            print(f"User {username} is already a member of the task '{AllProjects[position]["task"]["title"]}'.")
            else:
                raise PremissionError()
        except ProjectError as e:
            print(f"Error adding memeber: {e}")


    def RemoveMemberTask(self , username , requester , projectId):
        """_remove member from task_

        Args:
            username (_type_): _username_
            requester (_type_): _requester for add_
            projectId (_type_): _project id_

        Raises:
            PremissionError: _description_
        """
        try:
            idsData = Path('data/projectIds.json')
            AllprojectFile = Path('data') / f'project.json'
            datafile = Path('data') / f'project_{projectId}.json'
            with open(datafile , 'r') as f:
                project = json.load(f)
            with open(AllprojectFile , 'r') as f:
                AllProjects = json.load(f)
            if idsData.stat().st_size > 0:
                with open(idsData, 'r') as inputFile:
                    ids = json.load(inputFile)
                if projectId in ids:
                    position = ids.index(projectId)
            if requester == AllProjects[position]["leader"]:
                    if len(AllProjects) > 0:
                        i = 0 
                        for i in range(len(AllProjects[position]["task"]["assignees"])):
                            if username == AllProjects[position]["task"]["assignees"][i]:
                                time = datetime.now()
                                action = f"{username} remove from the task {AllProjects[position]["task"]["title"]}"
                                historyDict = self.ToDictHistory(requester , time , action)
                                AllProjects[position]["task"]["assignees"].pop(i)
                                project['tasks']['assignees'].pop(i)
                                AllProjects[position]["task"]["history"].append(historyDict)
                                project["task"]["history"].append(historyDict)
                                with open(AllprojectFile , 'w') as f:
                                    json.dump(AllProjects , f ,indent=4)
                                with open(datafile , 'w') as f:
                                    json.dump(project , f , indent=4)
                                print(f"User {username} remove from '{AllProjects[position]["task"]["title"]}'.")
                            else:
                                print(f"User {username} is not a member of the task '{AllProjects[position]["task"]["title"]}'.")
            else:
                raise PremissionError()
        except ProjectError as e:
            print(f"Error removing memeber: {e}")


    def AddComment(self , user , projectId):
        """Add comment to task

        Args:
            user (_type_): _username_
            projectId (_type_): _id of project_
        """
        try:
            description = input("Enter your comment:")
            AllprojectFile = Path('data') / f'project.json'
            datafile = Path('data') / f'project_{projectId}.json'
            with open(AllprojectFile , 'r') as f:
                AllProjects = json.load(f)
            with open(datafile , 'r') as f:
                project = json.load(f)
            i = 0
            time = datetime.now()
            commentDict = self.ToDictComment(description , user , time)
            for i in range(len(AllProjects)):
                if AllProjects[i]["id"] == projectId:
                    AllProjects[i]['tasks']['comments'].append(commentDict)
                    project['tasks']['comments'].append(commentDict)
                    with open(AllprojectFile , 'w') as f:
                        json.dump(AllProjects , f ,indent=4)
                    with open(datafile , 'w') as f:
                        json.dump(project , f , indent=4)
                    print(f"You successfully commented.")
        except Exception as e:
            print(f"Error commenting task: {e}")


    def UpdateTask(self , projectId , TaskId , username):
        """update and change task

        Args:
            projectId (_type_): _id of project_
            TaskId (_type_): _id of task_
            username (_type_): _username_
        """
        try:
            AllprojectFile = Path('data') / f'project.json'
            datafile = Path('data') / f'project_{projectId}.json'
            with open(AllprojectFile , 'r') as f:
                AllProjects = json.load(f)
            with open(datafile , 'r') as f:
                project = json.load(f)
            it = 0
            it1 = 0
            for it in range(len(AllProjects)):
                for it1 in range(len(AllProjects[it]["tasks"])):
                    if TaskId == AllProjects[it]["tasks"][it1]["id"]:
                        if username in AllProjects[it]["tasks"][it1]["members"]:
                            print("[1] Title")
                            print("[2] Description")
                            print("[3] Assignees")
                            print("[4] Priority")
                            print("[5] Status")
                            print("[6] Add Comment")
                            print("[7] Nothing")
                            choice = input("Which one you want to change?")

                            while True:
                                if choice == '1':
                                    newTitle = print("New Title:")
                                    i = 0
                                    for i in range(len(AllProjects)):
                                        if projectId == AllProjects[i]["id"]:
                                            j = 0 
                                            for j in range(len(AllProjects[i]["tasks"])):
                                                if TaskId == AllProjects[i]["tasks"][j]:
                                                    AllProjects[i]["tasks"][j]["title"] == newTitle
                                                    project["tasks"][j]["title"] == newTitle
                                                    with open(AllprojectFile , 'w') as f:
                                                        json.dump(AllProjects , f ,indent=4)
                                                    with open(datafile , 'w') as f:
                                                        json.dump(project , f , indent=4)

                                
                                elif choice == '2':
                                    newDes = print("New Description:")
                                    i = 0
                                    for i in range(len(AllProjects)):
                                        if projectId == AllProjects[i]["id"]:
                                            j = 0 
                                            for j in range(len(AllProjects[i]["tasks"])):
                                                if TaskId == AllProjects[i]["tasks"][j]:
                                                    AllProjects[i]["tasks"][j]["description"] == newDes
                                                    project["tasks"][j]["description"] == newDes
                                                    with open(AllprojectFile , 'w') as f:
                                                        json.dump(AllProjects , f ,indent=4)
                                                    with open(datafile , 'w') as f:
                                                        json.dump(project , f , indent=4)

                                elif choice == '3':
                                    choice1 = input("Do you want to remove or add someone? r(for remove)/a(for add)")
                                    user = input("Enter the ID of the person you want:")
                                    while True:
                                        if choice1 == 'r':
                                            self.RemoveMemberTask(user , username , projectId)
                                            break
                                        elif choice1 == 'a':
                                            self.AddMemberToTask(user , username , projectId)
                                            break
                                        else:
                                            print("Invalid choice.Pleas try again.")
                                            input(choice1)

                                elif choice == '4':
                                    try:
                                        print("[1] CRITICAL")
                                        print("[2] HIGH")
                                        print("[3] MEDIUM")
                                        print("[4] LOW")
                                        ListP = ["CRITICAL" , "HIGH" , "MEDIUM" , "LOW"]
                                        number = input("Which one you choose?")
                                        while True:
                                            if int(number) < 1 and int(number) > 4:
                                                print("Invalid choice.Pleas try again.")
                                                input(number)
                                            else:
                                                break
                                        newPriority = ListP.index(int(number) - 1)
                                        i = 0
                                        for i in range(len(AllProjects)):
                                            if projectId == AllProjects[i]["id"]:
                                                j = 0 
                                                for j in range(len(AllProjects[i]["tasks"])):
                                                    if TaskId == AllProjects[i]["tasks"][j]:
                                                        oldPriority = AllProjects[i]["tasks"][j]["priority"]
                                                        time = datetime.now()
                                                        action = f"{username} change priority from {oldPriority} to {newPriority}"
                                                        historyDict = self.ToDictHistory(username , time , action)
                                                        AllProjects[i]["task"]["history"].append(historyDict)
                                                        AllProjects[i]["tasks"][j]["priority"] == newPriority
                                                        project["tasks"][j]["priority"] == newPriority
                                                        with open(AllprojectFile , 'w') as f:
                                                            json.dump(AllProjects , f ,indent=4)
                                                        with open(datafile , 'w') as f:
                                                            json.dump(project , f , indent=4)
                                                        print("Priority changed successfully")
                                    except Exception as e:
                                        print(f"Error Changing Priority: {e}")
                                
                                elif choice == '5':
                                    try:
                                        print("[1] BACKLOG")
                                        print("[2] TODO")
                                        print("[3] DOING")
                                        print("[4] DONE")
                                        print("[5] ARCHIVED")
                                        ListP = ["BACKLOG" ,"TODO" , "DOING" , "DONE" , "ARCHIVED"]
                                        number = input("Which one you choose?")
                                        while True:
                                            if int(number) < 1 and int(number) > 5:
                                                print("Invalid choice.Pleas try again.")
                                                input(number)
                                            else:
                                                break
                                        newStatus = ListP.index(int(number) - 1)
                                        i = 0
                                        for i in range(len(AllProjects)):
                                            if projectId == AllProjects[i]["id"]:
                                                j = 0 
                                                for j in range(len(AllProjects[i]["tasks"])):
                                                    if TaskId == AllProjects[i]["tasks"][j]:
                                                        oldStatus = AllProjects[i]["tasks"][j]["status"]
                                                        time = datetime.now()
                                                        action = f"{username} change status from {oldStatus} to {newStatus}"
                                                        historyDict = self.ToDictHistory(username , time , action)
                                                        AllProjects[i]["task"]["history"].append(historyDict)
                                                        AllProjects[i]["tasks"][j]["status"] == newStatus
                                                        project["tasks"][j]["status"] == newStatus
                                                        with open(AllprojectFile , 'w') as f:
                                                            json.dump(AllProjects , f ,indent=4)
                                                        with open(datafile , 'w') as f:
                                                            json.dump(project , f , indent=4)
                                                        print("Status changed successfully")
                                    except Exception as e:
                                        print(f"Error Changing Status: {e}")
                    
                                elif choice == '6':
                                    self.AddComment(projectId , username)

                                elif choice == '7':
                                    break

                                else:
                                    print("Invalid choice.Pleas try again.")
                                    input(choice)
                        else:
                            print("You are not a member of this task.")
                            return
        except Exception as e:
            print(f"Error updating task: {e}")
    

    def DisplayTaskDetails(self, task , username , projectId):
        """Show of features of thask

        Args:
            task (_type_): _object or dict of task_
            username (_type_): _username_
            projectId (_type_): _id of project_
        """
        try:
            print(f"ID: {task["id"]}")
            print(f"Title: {task["title"]}")
            print(f"Description: {task["description"]}")
            print(f"Priority: {task["priority"]}")
            print(f"Status: {task["status"]}")
            print(f"Start Time: {task["startTime"]}")
            print(f"End Time: {task["endTime"]}")
            print(f"Assignees: {', '.join(task["assignees"])}")
            print(f"History: {', '.join(task["history"])}")
            print(f"Comment: {', '.join(task["comment"])}")

            answer = input("Do you want to edit this task? (y/n):")
            taskmanager = TaskManager()
            while True:
                if answer == 'y':
                    taskmanager.UpdateTask(projectId , task["id"] , username)
                    return
                elif answer == 'n':
                    return
                else:
                    print("Invalid choice.Pleas try again.")
                    input(answer)
        except Exception as e:
            print(f"Error displaying TaskDetails: {e}")
            
        
        
def TableTask(tasks , username , projectID): 
    """Show table of tasks

    Args:
        tasks (_type_): _object or dict of task_
        username (_type_): _username_
        projectID (_type_): _id of project_
    """
    try:
        taskManager = TaskManager()
        console = Console()
        table = Table(title="All Of Tasks In This Project:")
        table.add_column("BACKLOG" , justify="center", style="bold blue")
        table.add_column("TODO" , justify="center", style="bold blue")
        table.add_column("DOING" , justify="center", style="bold blue")
        table.add_column("DONE" , justify="center", style="bold blue")
        table.add_column("ARCHIVED" , justify="center", style="bold blue")
        taskss = {
            "BACKLOG" : [],
            "TODO" : [],
            "DOING" : [],
            "DONE" : [],
            "ARCHIVED" : []
        }
        i = 0
        for i in range(len(tasks)):
            if tasks[i]["priority"] == "BACKLOG":
                taskss["BACKLOG"].append(f"{tasks[i]["title"]}-{tasks[i]["id"]}")
            elif tasks[i]["priority"] == "TODO":
                taskss["TODO"].append(f"{tasks[i]["title"]}-{tasks[i]["id"]}")
            elif tasks[i]["priority"] == "DOING":
                taskss["DOING"].append(f"{tasks[i]["title"]}-{tasks[i]["id"]}")
            elif tasks[i]["priority"] == "DONE":
                taskss["DONE"].append(f"{tasks[i]["title"]}-{tasks[i]["id"]}")
            elif tasks[i]["priority"] == "ARCHIVED":
                taskss["ARCHIVED"].append(f"{tasks[i]["title"]}-{tasks[i]["id"]}")

        maxRows = max(len(taskss["TODO"]) , len(taskss["ARCHIVED"]) , len(taskss["BACKLOG"]) , len(taskss["DOING"]) , len(taskss["DONE"]))
        j = 0
        for j in range(maxRows):
            backlog = taskss["BACKLOG"] if j < len(taskss["BACKLOG"]) else ""
            todo = taskss["TODO"] if j < len(taskss["TODO"]) else ""
            doing = taskss["DOING"] if j < len(taskss["DOING"]) else ""
            done = taskss["DONE"] if j < len(taskss["DONE"]) else ""
            archived = taskss["ARCHIVED"] if j < len(taskss["ARCHIVED"]) else ""
            table.add_row(backlog , todo , doing , done , archived)

        console.print(table)
        if len(tasks) == 0:
            print("There is no task yet.")
            return
        else:
            print("Which task you choose?")
            print("[0] Non of them")
            while True:
                taskId = input("Enter id of task:")
                it = 0
                if taskId == '0':
                    return
                else:
                    temp = 0
                    for it in range(len(tasks)):
                        if tasks[it]["id"] == taskId:
                            temp += 1
                            taskManager.DisplayTaskDetails(tasks[it] , username , projectID)
                            return
                    if temp == 0:
                        print("Invalid Id.Pleas Try again.")

                
    except Exception as e:
        print(f"Error creating table : {e}")




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
        choice = input("Which one you choose?")
        while True:
            if int(choice) > int(temp) and int(choice) <= 0:
                print("Invalid choice.Pleas try again.")
                input(choice)
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
                print("This projects doesn't have any member")
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
                    print(f"{int(i + 1)}. {project["tasks"][i]}")

        elif choice == '3':
            print(f"Leader: {project["leader"]}")

        elif choice == '4':
            if len(project["tasks"]) == 0:
                print("There is no task yet")
            else:
                member = input("Enter member username: ")
                i = 0
                temp = 0
                for i in range(len(project["tasks"])):
                    if member in project["tasks"][i]["assignees"]:
                        temp += 1
                        print(f"{member} assigned to this task {project["tasks"][i]["title"]}")
                if temp == 0:
                    print(f"{username} assigned to none of the tasks")

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


if __name__ == "__main__":
    main()