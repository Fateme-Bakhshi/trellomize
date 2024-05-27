import json 
from pathlib import Path  

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
        return Project(data['title'] , data['id'] , data['leader'])
      
        

class ProjectManager(Project): #creat , find , load , add projects.be tore koli baraye modiriate projects
    def __init__(self):
        super().__init__(title = '' , projectId = '' , leader = '')
        self.projects = []

    def AddProject(self , title , projectId , leader):
        projectInfo = {
            'title': title,
            'id': projectId,
            'leader' : leader,
            'tasks' : [],
            'memnbers' : []
        }
        self.projects.append(projectInfo)
    def LoadProjects(self , projectId):
        try:
            datafile = Path('data') / f'project_{projectId}.json'
            with open(datafile,'r')as f:
                projectData = json.load(f)
                return [Project.FromDict(project) for project in projectData]
        except(FileNotFoundError,json.JSONDecodeError) as e:
            print(f"Error loading project: {e}")
            return [] 
        
    def SaveProject(self , project , projectId):
        try:
            datafile = Path('data') / f'project_{projectId}.json'
            with open(datafile,'a') as f:
                json.dump([project.ToDict()], f, indent=4)   
        except IOError as e:
            print(f"Error saving project : {e}")     
    
    def IsUnicId(self , projectID):
        if len(self.projects) == 0:
                return True
        else:
            for project in self.projects:
                if project.projectId == projectID:
                    return False
            return True
        
    def CreateProject(self):
        try:
            title = input("Enter project title: ")
            leader = input("Enter your username: ")
            while True:
                projectId = input("Enter project ID: ")
                while not projectId.isdigit():
                    print("Sorry.You can just use number for ID.")
                    projectId = input("Enter project ID: ")
                if self.IsUnicId(projectId):
                    project = Project(title , projectId , leader)
                    self.projects.append(project)
                    self.SaveProject(project , projectId)
                    print(f"Project '{title}' created successfully with Id {project.id} .")
                    break
                else:
                    raise ValueError(projectId)
        except Exception as e:
            print(f"Error creating project: {e}")


    def FindProject(self , projectId):
        try:
            if len(self.projects) == 0:
                print("You have not any project yet!")
            for project in self.projects:
                if project.id == projectId:
                    print("This project is found.")
                    return project
            raise NotFoundError(projectId)
        except Exception as e:
            print(f"Error finding project: {e}")
            return None
        
        

    def AddMemmber(self ,projectId , projectTitle , username , requester):
        try:
            project = self.FindProject(projectId)
            if project:
                if requester == project.leader:
                    if username not in project.members:
                        project.members.append(username)
                        self.SaveProject(project , projectId)
                        print(f"User {username} added to '{projectTitle}'.")
                    else:
                        print(f"User {username} is already a member of '{projectTitle}'.")
                else:
                    raise PremissionError()
            else:
                raise NotFoundError(projectTitle)
        except ProjectError as e:
            print(f"Error adding memeber: {e}")



    def RemoveMember(self , projectId , projectTitle , username , requester):
        try:
            project = self.FindProject(projectId)
            if project:
                if requester == project.leader:
                    self.projects.remove(project)
                    self.Project(project)
                    print(f"The member {username} removed successfully.")
                else:
                    raise PremissionError()
            else:
                raise NotFoundError(projectTitle)
        except ProjectError as e:
            print(f"Error removing memeber: {e}")



    def DeletProject(self , projectId , projectTitle , username , requester):
        try:
            project = self.FindProject(projectId)
            if project:
                if requester == project.leader:
                    if project.leader == username:
                        print("You can not remove yourself,you are leader!")
                    elif username in project.members:
                        project.members.remove(username)
                        self.SaveProject(project , projectId)
                        print(f"The project '{projectTitle}' deleted successfully.")
                    else:
                        print(f"User {username} is not a member of the project '{projectTitle}'.")
                else:
                    raise PremissionError()
            else:
                raise NotFoundError(projectTitle)
        except Exception as e:
            print(f"Error deleting project: {e}")


    def LeaderProjects(self , username):
        try:
            leaderProject = [project for project in self.projects if project.leader == username]
            if len(leaderProject) == 0:
                print("You are not a leader of any project.")
            else:
                return leaderProject
        except Exception as e:
            print(f"Error geting leader: {e}")


    def MemeberProject(self , username):
        try:
            memberPtoject = [project for project in self.projects if username in project.members and username != project.leader]
            if len(memberPtoject) == 0:
                print("You are not a member of any project.")
                return False
            else:
                return memberPtoject
        except Exception as e:
            print(f"Error getting memeber: {e}")

    def DisplayeProject(self , project):
        print(f"Project ID: {project.id}")
        print(f"Title: {project.title}")
        print(f"Leader: {project.leader}")
        print(f"Members: {''.join.project.members}")
        print(f"Tasks: {project.tasks}")

