# Trellomize
**Terminal-Based Project Management System**  
Developed as a mini-project for the Advanced Programming course  
Department of Mathematics and Computer Science
Iran University of Science and Technology — Spring 2024

---

## About the project
**Trellomize** is a terminal-based project and task management system developed in Python as a mini-project for the Advanced Programming course. Inspired by tools like Trello, this system allows users to manage projects, assign tasks, collaborate as a team, and monitor progress — all through a command-line interface.

It is implemented using object-oriented programming principles, and supports account management, project-role distinction, task tracking, logging, and data persistence.

---

## Features Overview
- ## Admin Management (via CLI)
- Initialize the system admin using manager.py with argparse
- Reset all system data via a purge command with confirmation prompt
- ## User Management
- Register new users (with validation for duplicate/invalid usernames or emails)
- Secure login/logout functionality
- Ability to disable/enable user accounts by admin
- ## Project Management
- Users can create projects and become their leaders
- Leaders can add/remove users to/from projects
- Clear distinction between leader and member roles
- View project list based on user role (leader/member)
- ## Task Management
- Add tasks to projects with the following fields:
- UUID-based unique task ID
- Title, description
- Start and end datetime (default: now and now+24h)
- Priority (CRITICAL, HIGH, MEDIUM, LOW)
- Status (BACKLOG, TODO, DOING, DONE, ARCHIVED)
- Assignees (members of the project)
- Commenting system (with timestamp and author)
- Action history for any changes in assignment, priority, status
- Project leaders can remove users from task assignments
- ## Terminal UI
- Uses the rich library for structured and colored output
- Tabular task overview grouped by status
- ## Security & Storage
- Passwords hashed using SHA-256
- Data saved in structured JSON files for portability
- ## Logging System
- Major actions (user creation, login, project/task modifications) are logged
- ## Testing
- Includes unit tests using Python’s unittest module
  
---

## Getting Started
1. **Create and activate a virtual environment** (Python 3.11+)
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set up admin user:**
   ```bash
   python ./manager.py create-admin --username (admin's username) --password (admin's password)
   ```
4. **Run the program:**
   ```bash
   python mainn.py
   ```
   
---

## Project Structure
```bash
trellomize-1.0/
├── mainn.py                 
├── manager.py
├── pt_test.py             
├── Users/
│   ├── user.py            
│   └── validation.py        
├── Projects_And_Tasks/
│   ├── Projects_menu.py      
│   ├── task.py
│   ├── project.py
│  └── pm2.py        
├── Users_Data/
│   └── Users/            
├── Projects_Data/           
└── logFile/                
```

---

## Team members

- Yasaman Saffar Tabasi  
- Fateme Bakhshi

### Notes

• Do not delete or rename system folders (`Users_Data`, `Projects_Data`, `logFile`)  
• The project uses a JSON-based storage system (no database required)  
• Final submission is tagged as `v1.0` in the Releases section  
• This project was developed as the second course project for the "Advanced Programming" class at IUST (Spring 1403)

