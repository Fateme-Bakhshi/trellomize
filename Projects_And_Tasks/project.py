import json #for save file
from pathlib import Path  #for save file
import os, logging
from rich.console import Console
from rich.table import Table

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
        console = Console()
        try:
            if self.findId(projectId):
                project = Project(title , projectId , leader)
                project = project.ToDict()
                project["leader"] = leader
                project["members"].append(leader)
                self.SaveProject(project)
                console.print(f"\nProject '{title}' created successfully with Id {projectId} .", style='bold deep_sky_blue1')
                return True
            else:
                raise ValueError(projectId)
        except Exception as e:
            console.print(f"\nError adding project: {e}", style='dark_orange')

        
    def SaveProject(self , project):
        """_save project to jsonFile_

        Args:
            project (_type_): _dict or object_
        """
        console = Console()
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
            console.print(f"\nError saving project: {e}", style='dark_orange')    


        
    def CreateProject(self, leader):
        """
            creat project
        """
        console = Console()
        try:
            title = input("Enter project title: ")
            leader = leader.username
            while True:
                projectId = input("Enter project ID: ")
                while not projectId.isdigit():
                    console.print("\nSorry.You can just use number for ID.", style='dark_orange') 
                    projectId = input("Enter project ID: ")
                    break
                while len(projectId) < 4:
                    console.print("\nYour project ID must be atleast 4 digits.", style='dark_orange') 
                    projectId = input("Enter project ID: ")
                    break
                if(self.AddProject(title , projectId , leader)):
                    logging.info(f'{leader} added a new project with {title} title and {projectId} id.')
                    break
        except Exception as e:
            console.print(f"\nError creating project: {e}", style='dark_orange') 


   
    def FindProject(self , projectId , username):
        """

        Args:
            projectId (_type_): _id of project_
            username (_type_): _user_

        Returns:
            _type_: _description_
        """
        console = Console()
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
                                console.print(f"\nThis project is found.", style='bold deep_sky_blue1')
                    return projectId
                else:
                    return False
            else:
                console.print("\nYou have no projects yet!", style='dark_orange')
                return False
        except Exception as e:
            console.print(f"\nError finding project: {e}", style='dark_orange') 
        
        
    
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
        console = Console()
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
                        console.print(f"\nUser {username} added to '{projectTitle}'.", style='bold deep_sky_blue1')
                        logging.info(f"User {username} added to '{projectTitle}'.")
                    else:
                        console.print(f"\nUser {username} is already a member of the project '{projectTitle}'.", style='dark_orange') 
            else:
                raise PremissionError()
        except ProjectError as e:
            console.print(f"\nError adding memeber: {e}", style='dark_orange') 


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
        console = Console()
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
                    console.print(f"\nSorry.You are leader.You can not remove yourself.", style='dark_orange') 
                else:
                    if len(AllProjects) > 0:
                        i = 0
                        temp = 0
                        for i in range(len(AllProjects[position]["members"])):
                            if username == AllProjects[position]["members"][i]:
                                temp += 1
                                AllProjects[position]["members"].pop(i)
                                project1["members"].pop(i)
                                with open(AllprojectFile , 'w') as f:
                                    json.dump(AllProjects , f ,indent=4)
                                with open(datafile , 'w') as f:
                                    json.dump(project1 , f , indent=4)
                                console.print(f"\nUser {username} successfully removed from '{projectTitle}'.", style='bold deep_sky_blue1')
                                logging.info(f"User {username} removed from '{projectTitle}'.")
                        if temp == 0:
                            console.print(f"\nUser {username} is not a member of the project '{projectTitle}'.", style='dark_orange') 
                        return
            else:
                raise PremissionError()
        except ProjectError as e:
            console.print(f"\nError removing memeber: {e}", style='dark_orange') 


    def DeletProject(self , projectId , projectTitle , requester):
        """
        Args:
            projectId (_type_): _id of project_
            projectTitle (_type_): _title of project_
            requester (_type_): _requester for delet project_

        Raises:
            PremissionError: _description_
        """
        console = Console()
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
                    console.print(f"\nThe project '{projectTitle}' deleted successfully.", style='bold deep_sky_blue1')
                    logging.info(f"The project '{projectTitle}' deleted.")
                else:
                    raise PremissionError()
        except Exception as e:
            console.print(f"\nError deleting project: {e}", style='dark_orange')

   
    def LeaderProjects(self , username):
        """_show list of projects that user a leader of those_

        Args:
            username (_type_): _username_
        """
        console = Console()
        try:
            all_project_file = self.data_folder / 'project.json'
            if os.path.exists(all_project_file):
                with open(all_project_file, 'r') as file:
                    all_projects = json.load(file)

                if len(all_projects) > 0:
                    project_table = Table(show_header=True, header_style="bold magenta")
                    project_table.add_column("Title", style="dim", width=12)
                    project_table.add_column("ID", style="dim", width=12)

                    found = False
                    for project in all_projects:
                        if username == project["leader"]:
                            project_table.add_row(project['title'], str(project['id']))
                            found = True

                    if found:
                        console.print(project_table)
                    else:
                        console.print("\nYou are not a leader of any project.", style='dark_orange')
                else:
                    console.print("There are no projects yet.")
            else:
                console.print('There are no projects yet.')
        except Exception as e:
            console.print(f"\nError showing project member: {e}", style='dark_orange')
    
    def MemeberProject(self , username):
        """_show list of projects that user just a member of those_

        Args:
            username (_type_): _username_
        """
        console = Console()
        try:
            all_project_file = self.data_folder / 'project.json'
            if os.path.exists(all_project_file):
                with open(all_project_file, 'r') as file:
                    all_projects = json.load(file)

                project_table = Table(show_header=True, header_style="bold magenta")
                project_table.add_column("Title", style="dim", width=20)
                project_table.add_column("ID", style="dim", width=12)

                found = False
                for project in all_projects:
                    for member in project["members"]:
                        if username == member and username != project["leader"]:
                            project_table.add_row(project['title'], str(project['id']))
                            found = True
                            break

                if found:
                    console.print(project_table)
                else:
                    console.print("\nYou are not a member of any project.", style='dark_orange')
            else:
                console.print('There are no projects yet.')
        except Exception as e:
            console.print(f"\nError showing project member: {e}", style='dark_orange')
