
import json, uuid #for save file #for unic id
from pathlib import Path  #for save file
from datetime import datetime,timedelta #for time
from enum import Enum #for Enum Class
from rich.console import Console #for table
from rich.table import Table
from .project import ProjectError
from .project import PremissionError
import os, logging
from Users.user import UserManager

idsData = Path('Projects_Data/projectIds.json')
AllprojectFile = Path('Projects_Data/project.json')

logging.basicConfig(filename="logFile/actions.log", format='%(asctime)s - %(message)s', filemode='a', level=logging.DEBUG)

def clear_screen():
    os.system('cls')
    
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
        self.id = str(uuid.uuid4().int)[:4]
        self.title = ""
        self.description = ""
        self.startTime = datetime.now() 
        self.endTime = self.startTime + timedelta(days=1)
        self.assignees = []
        self.priority = Priority.LOW.value
        self.status = Status.BACKLOG.value
        self.history = []
        self.comments = []


    def ToDictTask(self):
        return{
            'id' : self.id,
            'title' : self.title,
            'description' : self.description,
            'startTime' : self.startTime.isoformat(),
            'endTime' : self.endTime.isoformat(),
            'assigners' : self.assignees,
            'priority' : self.priority,
            'status' : self.status,
            'history' : self.history,
            'comments' : self.comments
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
        super().__init__()


    def CreatTask(self , projectId):
        """creat new task

        Args:
            projectId (_type_): _id of project_
        """
        try:
            task = TaskManager()
            answer1 = input("Do you want to write title for task? y/n  ")
            while True:
                if answer1 == 'y':
                    title = input("Enter title: ")
                    task.title = title
                    break
                elif answer1 == 'n':
                    break
                elif answer1 != 'n':
                    print("Invalid answer.Pleas try again.")
                    answer1 = input()
            answer2 = input("Do you want to write description? y/n  ")
            while True:
                if answer2 == 'y':
                    description = input("Enter description: ")
                    task.description = description
                    break
                elif answer2 == 'n':
                    break
                elif answer2 != 'n':
                    print("Invalid answer.Please try again.")
                    answer2 = input()
            datafile = Path('Projects_Data') / f'project_{projectId}.json'
            with open(AllprojectFile , 'r') as f:
                AllProjects = json.load(f)
            task.ToDictTask()
            i = 0
            for i in range(len(AllProjects)):
                if AllProjects[i]["id"] == projectId:
                    if task not in AllProjects[i]["tasks"]:
                        AllProjects[i]["tasks"].append(task.ToDictTask())
                        with open(datafile,'r') as f:
                            project = json.load(f)
                        project["tasks"].append(task.ToDictTask())
                        position = len(AllProjects[i]["tasks"])
                        with open(datafile , 'w') as f:
                            json.dump(project , f , indent=4)
                        with open(AllprojectFile , 'w') as f:
                            json.dump(AllProjects , f , indent=4)
                        print(f'Task "{AllProjects[i]["tasks"][int(position) - 1]["title"]}" created successfully with Id {AllProjects[i]["tasks"][int(position) - 1]["id"]}.')
                        logging.info(f'Task "{AllProjects[i]["tasks"][int(position) - 1]["title"]}" created successfully with Id {AllProjects[i]["tasks"][int(position) - 1]["id"]}.')
                        break
        except Exception as e:
            print(f"Error creating task: {e}")



    def AddMemberToTask(self ,username , requester , projectId , TaskId):
        """_Assign member to task_

        Args:
            username (_type_): _username_
            requester (_type_): _requester for add_
            projectId (_type_): _project id_

        Raises:
            PremissionError: _description_
        """
        try:
            datafile = Path('Projects_Data') / f'project_{projectId}.json'
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
                        for j in range(len(AllProjects[position]["tasks"])):
                            if TaskId == AllProjects[position]["tasks"][j]["id"]:
                                if username not in AllProjects[position]["tasks"][j]["assigners"]:
                                    AllProjects[position]["tasks"][j]["assigners"].append(username)
                                    time = str(datetime.now())
                                    action = f'{username} add to the task {AllProjects[position]["tasks"][j]["title"]}.'
                                    historyDict = self.ToDictHistory(requester , time , action)
                                    AllProjects[position]["tasks"][j]["history"].append(historyDict)
                                    project["tasks"][j]["assigners"].append(username)
                                    project["tasks"][j]["history"].append(historyDict)
                                    with open(AllprojectFile , 'w') as f:
                                        json.dump(AllProjects , f ,indent=4)
                                    with open(datafile , 'w') as f:
                                        json.dump(project , f , indent=4)
                                    print(f'User "{username}" added to "{AllProjects[position]["tasks"][j]["title"]}".')
                                    logging.info(f'User "{username}" added to "{AllProjects[position]["tasks"][j]["title"]}" task.')
                                    return
                                else:
                                    print(f'User {username} is already a member of the task "{AllProjects[position]["tasks"][j]["title"]}".')
                                    return
            else:
                raise PremissionError()
        except ProjectError as e:
            print(f"Error adding memeber: {e}")


    def RemoveMemberTask(self , username , requester , projectId , TaskId):
        """_remove member from task_

        Args:
            username (_type_): _username_
            requester (_type_): _requester for add_
            projectId (_type_): _project id_

        Raises:
            PremissionError: _description_
        """
        try:
            datafile = Path('Projects_Data') / f'project_{projectId}.json'
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
                        temp = 0
                        for j in range(len(AllProjects[position]["tasks"])):
                                if TaskId == AllProjects[position]["tasks"][j]["id"]:
                                    for i in range(len(AllProjects[position]["tasks"][j]["assigners"])):
                                        if username == AllProjects[position]["tasks"][j]["assigners"][i]:
                                            temp += 1
                                            time = str(datetime.now())
                                            action = f'{username} remove from the task {AllProjects[position]["tasks"][j]["title"]}'
                                            historyDict = self.ToDictHistory(requester , time , action)
                                            AllProjects[position]["tasks"][j]["assigners"].pop(i)
                                            project['tasks'][j]['assigners'].pop(i)
                                            AllProjects[position]["tasks"][j]["history"].append(historyDict)
                                            project["tasks"][j]["history"].append(historyDict)
                                            with open(AllprojectFile , 'w') as f:
                                                json.dump(AllProjects , f ,indent=4)
                                            with open(datafile , 'w') as f:
                                                json.dump(project , f , indent=4)
                                            print(f'User {username} removed from "{AllProjects[position]["tasks"][j]["title"]}"".')
                                            logging.info(f'User "{username}" removed from "{AllProjects[position]["tasks"][j]["title"]}" task.')
                                            return
                                    if temp == 0:
                                        print(f'User {username} is not a member of the task "{AllProjects[position]["tasks"][j]["title"]}".')
                                        return
            else:
                raise PremissionError()
        except ProjectError as e:
            print(f"Error removing memeber: {e}")


    def AddComment(self , user , projectId , TaskId):
        """Add comment to task

        Args:
            user (_type_): _username_
            projectId (_type_): _id of project_
        """
        try:
            description = input("Enter your comment:")
            datafile = Path('Projects_Data') / f'project_{projectId}.json'
            with open(AllprojectFile , 'r') as f:
                AllProjects = json.load(f)
            with open(datafile , 'r') as f:
                project = json.load(f)
            i = 0
            time = str(datetime.now())
            commentDict = self.ToDictComment(description , user , time)
            for i in range(len(AllProjects)):
                if AllProjects[i]["id"] == projectId:
                    for j in range(len(AllProjects[i]["tasks"])):
                        if TaskId == AllProjects[i]["tasks"][j]["id"]:
                            AllProjects[i]['tasks'][j]['comments'].append(commentDict)
                            project['tasks'][j]['comments'].append(commentDict)
                            with open(AllprojectFile , 'w') as f:
                                json.dump(AllProjects , f ,indent=4)
                            with open(datafile , 'w') as f:
                                json.dump(project , f , indent=4)
                            print(f"You successfully commented.")
                            logging.info(f"'{user}' commented on '{AllProjects[i]['tasks'][j]['title']}' task.")
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
            datafile = Path('Projects_Data') / f'project_{projectId}.json'
            with open(AllprojectFile , 'r') as f:
                AllProjects = json.load(f)
            with open(datafile , 'r') as f:
                project = json.load(f)
            it = 0
            it1 = 0
            for it in range(len(AllProjects)):
                for it1 in range(len(AllProjects[it]["tasks"])):
                    if TaskId == AllProjects[it]["tasks"][it1]["id"]:
                        if username in AllProjects[it]["tasks"][it1]["assigners"] or username == AllProjects[it]["leader"]:
                            print("\n")
                            print("[1] Title")
                            print("[2] Description")
                            print("[3] Assigners")
                            print("[4] Priority")
                            print("[5] Status")
                            print("[6] Add Comment")
                            print("[7] Nothing")
                            choice = input("Which one you want to change?")

                            while True:
                                if choice == '1':
                                    newTitle = input("New Title:")
                                    i = 0
                                    for i in range(len(AllProjects)):
                                        if projectId == AllProjects[i]["id"]:
                                            j = 0 
                                            for j in range(len(AllProjects[i]["tasks"])):
                                                if TaskId == AllProjects[i]["tasks"][j]["id"]:
                                                    AllProjects[i]["tasks"][j]["title"] = newTitle
                                                    project["tasks"][j]["title"] = newTitle
                                                    with open(AllprojectFile , 'w') as f:
                                                        json.dump(AllProjects , f ,indent=4)
                                                    with open(datafile , 'w') as f:
                                                        json.dump(project , f , indent=4)
                                                    print("Title changed successfully")
                                                    logging.info(f'task "{AllProjects[i]["tasks"][j]["title"]}" changed to "{newTitle}".')
                                                    return
                                                        

                                
                                elif choice == '2':
                                    newDes = input("New Description:")
                                    i = 0
                                    for i in range(len(AllProjects)):
                                        if projectId == AllProjects[i]["id"]:
                                            j = 0 
                                            for j in range(len(AllProjects[i]["tasks"])):
                                                if TaskId == AllProjects[i]["tasks"][j]["id"]:
                                                    AllProjects[i]["tasks"][j]["description"] = newDes
                                                    project["tasks"][j]["description"] = newDes
                                                    with open(AllprojectFile , 'w') as f:
                                                        json.dump(AllProjects , f ,indent=4)
                                                    with open(datafile , 'w') as f:
                                                        json.dump(project , f , indent=4)
                                                    print("description changed successfully")
                                                    logging.info(f'description "{AllProjects[i]["tasks"][j]["description"]}" changed to "{newDes}".')
                                                    return
                                                        

                                elif choice == '3':
                                    if username == AllProjects[it]["leader"]:
                                        user_manager = UserManager()
                                        user = input("Enter the ID of the person you want to remove or add:")
                                        if not user_manager.find_user(user):
                                            print('Username does not exist.')
                                            return
                                        else:
                                            choice1 = input("Do you want to remove or add? r(for remove)/a(for add)")
                                            while True:
                                                if choice1 == 'r':
                                                    self.RemoveMemberTask(user , username , projectId , AllProjects[it]["tasks"][it1]["id"])
                                                    
                                                    return
                                                elif choice1 == 'a':
                                                    self.AddMemberToTask(user , username , projectId , AllProjects[it]["tasks"][it1]["id"])
                                                    return
                                                else:
                                                    print("Invalid choice.Please try again.")
                                                    choice1 = input()
                                    else:
                                        print("Sorry.you are not leader.")
                                        break

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
                                                number = input()
                                            else:
                                                break
                                        newPriority = ListP[int(number) - 1]
                                        i = 0
                                        for i in range(len(AllProjects)):
                                            if projectId == AllProjects[i]["id"]:
                                                j = 0 
                                                for j in range(len(AllProjects[i]["tasks"])):
                                                    if TaskId == AllProjects[i]["tasks"][j]["id"]:
                                                        oldPriority = AllProjects[i]["tasks"][j]["priority"]
                                                        time = str(datetime.now())
                                                        action = f"{username} change priority from {oldPriority} to {newPriority}"
                                                        historyDict = self.ToDictHistory(username , time , action)
                                                        AllProjects[i]["tasks"][j]["history"].append(historyDict)
                                                        AllProjects[i]["tasks"][j]["priority"] = newPriority
                                                        project["tasks"][j]["priority"] = newPriority
                                                        project["tasks"][j]["history"].append(historyDict)
                                                        with open(AllprojectFile , 'w') as f:
                                                            json.dump(AllProjects , f ,indent=4)
                                                        with open(datafile , 'w') as f:
                                                            json.dump(project , f , indent=4)
                                                        print("Priority changed successfully")
                                                        logging.info(f'Priority changed from "{project["tasks"][j]["priority"]}" to "{newPriority}".')
                                                        return
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
                                                number = input()
                                            else:
                                                break
                                        newStatus = ListP[int(number) - 1]
                                        i = 0
                                        for i in range(len(AllProjects)):
                                            if projectId == AllProjects[i]["id"]:
                                                j = 0 
                                                for j in range(len(AllProjects[i]["tasks"])):
                                                    if TaskId == AllProjects[i]["tasks"][j]["id"]:
                                                        oldStatus = AllProjects[i]["tasks"][j]["status"]
                                                        time = str(datetime.now())
                                                        action = f"{username} change status from {oldStatus} to {newStatus}"
                                                        historyDict = self.ToDictHistory(username , time , action)
                                                        AllProjects[i]["tasks"][j]["history"].append(historyDict)
                                                        AllProjects[i]["tasks"][j]["status"] = newStatus
                                                        project["tasks"][j]["status"] = newStatus
                                                        project["tasks"][j]["history"].append(historyDict)
                                                        with open(AllprojectFile , 'w') as f:
                                                            json.dump(AllProjects , f ,indent=4)
                                                        with open(datafile , 'w') as f:
                                                            json.dump(project , f , indent=4)
                                                        print("Status changed successfully")
                                                        logging.info(f'Status changed from "{project["tasks"][j]["status"]}" to "{newStatus}".')
                                                        return
                                    except Exception as e:
                                        print(f"Error Changing Status: {e}")
                    
                                elif choice == '6':
                                    self.AddComment(username , projectId , AllProjects[it]["tasks"][it1]["id"])
                                    break

                                elif choice == '7':
                                    break

                                else:
                                    print("Invalid choice.Pleas try again.")
                                    choice = input()
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
        clear_screen()
        try:
            print("\n")
            print(f' ID: {task["id"]}')
            print(f' Title: {task["title"]}')
            print(f' Description: {task["description"]}')
            print(f' Priority: {task["priority"]}')
            print(f' Status: {task["status"]}')
            print(f' Start Time: {task["startTime"]}')
            print(f' End Time: {task["endTime"]}')
            print(f' Assigners: {", ".join(task["assigners"])}')
            print(" History:")
            for i in range(len(task["history"])):
                print(f"{int(i) + 1}.")
                print(f'  User : {task["history"][i]["user"]}')
                print(f'  Description : {task["history"][i]["action"]}')
            print(" Comments:")
            for j in range(len(task["comments"])):
                print(f"{int(j) + 1}.")
                print(f'  User : {task["comments"][j]["user"]}')
                print(f'  Description : {task["comments"][j]["description"]}')
    
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
                    answer = input()
        except Exception as e:
            print(f"Error displaying TaskDetails: {e}")
            
        
        
def TableTask(tasks , username , projectID): 
    """Show table of tasks

    Args:
        tasks (_type_): _object or dict of task_
        username (_type_): _username_
        projectID (_type_): _id of project_
    """
    clear_screen()
    try:
        taskManager = TaskManager()
        console = Console()
        table = Table(title="All Of Tasks In This Project:")
        ListBack=[]
        ListTodo = []
        ListDoing =[]
        ListDone=[]
        ListArchived=[]
        it1 = 0
        for it1 in range(len(tasks)):
            if tasks[it1]["status"] == 'BACKLOG':
                ListBack.append(f'{tasks[it1]["title"]}-{tasks[it1]["id"]}')
            elif tasks[it1]["status"] == 'TODO':
                ListTodo.append(f'{tasks[it1]["title"]}-{tasks[it1]["id"]}')
            elif tasks[it1]["status"] == 'DOING':
                ListDoing.append(f'{tasks[it1]["title"]}-{tasks[it1]["id"]}')
            elif tasks[it1]["status"] == 'DONE':
                ListDone.append(f'{tasks[it1]["title"]}-{tasks[it1]["id"]}')
            elif tasks[it1]["status"] == 'ARCHIVED':
                ListArchived.append(f'{tasks[it1]["title"]}-{tasks[it1]["id"]}')
        table.add_column("BACKLOG", justify="center", style="bold blue")
        table.add_column("TODO", justify="center", style="bold blue")
        table.add_column("DOING", justify="center", style="bold blue")
        table.add_column("DONE", justify="center", style="bold blue")
        table.add_column("ARCHIVED", justify="center", style="bold blue")
        maxLength = max(len(ListBack), len(ListTodo), len(ListDoing), len(ListDone), len(ListArchived))
        for i in range(maxLength):
            backlog = ListBack[i] if i < len(ListBack) else ""
            todo = ListTodo[i] if i < len(ListTodo) else ""
            doing = ListDoing[i] if i < len(ListDoing) else ""
            done = ListDone[i] if i < len(ListDone) else ""
            archived = ListArchived[i] if i < len(ListArchived) else ""
            table.add_row(backlog, todo, doing, done, archived) 
    

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
