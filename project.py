import json #for save file
from pathlib import Path  #for save file
import os, logging

logging.basicConfig(filename="logFile/actions.log", format='%(asctime)s - %(message)s', filemode='a', level=logging.DEBUG)

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


def clear_screen():
    os.system('cls')

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
        self.data_folder = Path('Projects_Data')
        self.data_folder.mkdir(parents=True, exist_ok=True)


    def findId(self, projectId):
        """
        Args:
            projectId (_type_): _id of project_

        Returns:
            _type_: _description_
        """
        idsData = Path('Projects_Data/projectIds.json')
        if os.path.exists(idsData):
            if idsData.stat().st_size > 0:
                with open(idsData, 'r') as inputFile:
                    ids = json.load(inputFile)
                    for id in ids:
                        if projectId == id:
                            return False
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
            AllprojectFile = self.data_folder / 'project.json'
            datafile = self.data_folder / f"project_{project['id']}.json"
            idData = Path('Projects_Data/projectIds.json')
            if not isinstance(project , dict):
                project = project.ToDict()
        
            with open(datafile,'w') as f:
                json.dump(project, f)  
                
            project_list = []
            if os.path.exists(AllprojectFile):
                with open(AllprojectFile, 'r') as f:
                    project_list = json.load(f)
            project_list.append(project)
            with open(AllprojectFile,'w') as f:
                json.dump(project_list, f, indent=4)
            ids = []
            if os.path.exists(idData):
                with open(idData, 'r') as idFile:
                    ids = json.load(idFile)
                    if not(project["id"] in ids):
                        ids.append(project["id"])
            with open(idData, 'w') as id: 
                json.dump(ids , id)
        except IOError as e:
            print(f"Error saving project : {e}")     


        
    def CreateProject(self, leader):
        """
            creat project
        """
        try:
            title = input("Enter project title: ")
            leader = leader.username
            while True:
                projectId = input("Enter project ID: ")
                while not projectId.isdigit():
                    print("Sorry.You can just use number for ID.")
                    projectId = input("Enter project ID: ")
                    break
                while len(projectId) < 4:
                    print("Your project ID must be atleast 4 digits")
                    projectId = input("Enter project ID: ")
                    break
                if(self.AddProject(title , projectId , leader)):
                    logging.info(f'{leader} added a new project with {title} title and {projectId} id.')
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
            idsData = Path('Projects_Data/projectIds.json')
            AllprojectFile = self.data_folder / f'project.json'
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
            idsData = Path('Projects_Data/projectIds.json')
            AllprojectFile = self.data_folder / f'project.json'
            datafile = self.data_folder / f'project_{projectId}.json'
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
            idsData = Path('Projects_Data/projectIds.json')
            AllprojectFile = self.data_folder / f'project.json'
            datafile = self.data_folder / f'project_{projectId}.json'
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
            idsData = Path('Projects_Data/projectIds.json')
            AllprojectFile = self.data_folder / f'project.json'
            dataFile = self.data_folder/f'project_{projectId}.json'
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
                    dataFile.unlink()
                    with open(AllprojectFile , 'w') as f:
                        json.dump(AllProjects , f ,indent=4)
                    with open(idsData , 'w') as f:
                        json.dump(ids , f , indent=4)
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
        clear_screen()
        try:
            AllprojectFile = self.data_folder / f'project.json'
            with open(AllprojectFile , 'r') as f:
                AllProjects = json.load(f)
            it = 0
            if len(AllProjects) > 0:
                temp = 0
                for it in range(len(AllProjects)):
                    if username == AllProjects[it]["leader"]:
                        print(f"{AllProjects[it]['title']} / ID : {AllProjects[it]['id']}")
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
        clear_screen()
        try:
            AllprojectFile = Path('Projects_Data') / f'project.json'
            with open(AllprojectFile , 'r') as f:
                AllProjects = json.load(f)
            it = 0
            if len(AllProjects) > 0:
                for it in range(len(AllProjects)):
                    i = 0
                    temp = 0
                    for i in range(len(AllProjects[it]["members"])):
                        if username == AllProjects[it]["members"][i] and username != AllProjects[it]["leader"]:
                            print(f"{AllProjects[it]['title']} / ID : {AllProjects[it]['id']}")
                            temp += 1
                if temp == 0:
                    print("You are not a member of any project.")
        except Exception as e:
            print(f"Error Showing project member: {e}")
