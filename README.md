# Trellomize
**Terminal-Based Project Management System**  
Developed as a mini-project for the Advanced Programming course  
Department of Mathematics and Computer Science
Iran University of Science and Technology — Spring 2024

## About the project
**Trellomize** is a simple command-line project and task management system, designed with a focus on **object-oriented programming principles**. Users can create accounts, define projects, assign team members, and manage tasks collaboratively through a terminal-based interface.

## Key Features
- Admin setup and data reset via CLI (`argparse`)
- User registration and login with validation
- Project creation and team management (Leader vs. Member roles)
- Task creation with priority, status, assignees, comments, and history
- Rich terminal UI using the `rich` library
- Secure password hashing and data storage in JSON
- Action logging using `logging`
- Unit testing with `unittest`

## Getting Started
1. Create and activate a virtual environment (Python 3.11+)
2. 2. Install dependencies:
```
pip install -r requirements.txt
```
3.Set up admin user:
```
python ./manager.py create-admin --username (admin's username) --password (admin's password)
```
4.Run the program:
```
python mainn.py
```

## Team members
-Yasaman Saffar Tabasi
-Fateme Bakhshi

##
Final submission tagged as v1.0 in the Releases section
