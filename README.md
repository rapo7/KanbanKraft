# KanbanKraft

## About The Project

KanbanKraft is a dynamic, user-friendly Kanban board application designed to streamline project management and team collaboration. With its intuitive interface and powerful features, KanbanKraft allows teams to visualize workflow, track project progress, and identify bottlenecks in real-time.

### Features

- Drag-and-drop tasks between different stages of your workflow
- Customizable board lists to match your project's stages
- Real-time collaboration for teams
- Task assignments, deadlines, and descriptions

## Getting Started

This section should provide instructions on setting up the project locally. Here, you could include steps for cloning the repo, installing dependencies, and any required environment setup.

### Prerequisites

- Node.js (v14 or newer recommended)
- Python (v3.0 or newer)
- Django (latest version)

### Installation
1. Install Git , Python
2. Clone the repository:
   ```sh
   git clone https://github.com/rapo7/kanbanKraft.git
   cd kanbanKraft
   ```
3. Make a virtual env
   ```sh
   python3 -m venv venv
4. Activate the `venv` for Mac
   ```sh
   source venv/bin/activate
   ```
   For Windows execute
   ```cmd
   venv/Scripts/activate
   ```
5. Install Required Packages
   ```sh
   pip3 install -r requirements.txt
   ```
6. Make Migrations
  ```sh
  python3 manage.py makemigrations
  ```
7. Migrate
  ```sh
  python3 manage.py migrate
  ```
8. Create Sample Users
  ```sh
  python3 manage.py create_dummy_users
  ```
9. Create Sample Projects and Tasks
  ```sh
  python3 manage.py populate_projects
  ```
10. Create Super User
  ```sh
  python3 manage.py createsuperuser
  ```
11. Run the project
 ```sh
  python3 manage.py runserver
  ```
12. Open the url `http://localhost:8000` in the browser 
   
