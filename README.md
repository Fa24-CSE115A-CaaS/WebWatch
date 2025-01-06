# What is WebWatch?
## Project Motivation and Team
WebWatch was a project built for CSE115A: Introduction to Software Engineering at UC Santa Cruz in Fall 2024.

Our team consists of [Cameron Candau](https://github.com/Cam-Can-Do) (Product Owner), [Alex Kekchidis](https://github.com/akekchid), [Isaac To](https://github.com/Isaac-To), [Jordan Nguy](https://github.com/Jordan-Nguy), [Leonardo Gallego](https://github.com/leonardogs1), and [Simon Zhao](https://github.com/SimonZhao7). 

The concept arose from our personal experiences in [obtaining parking permits at UCSC](https://ucsc.aimsparking.com/permits/?cmd=new).

## The Problem
The web often used for sharing time-sensitive opportunities which lack built-in notification systems. Manually refreshing a webpage while anticipating its change drains valuable time and energy from the user.

## Our Solution
WebWatch is a web application that enables users to monitor other webpages for changes.
![WebWatch home](https://github.com/user-attachments/assets/972baa44-8798-428e-8855-ee3f200c329c)

Our core functionality included four primary features, all of which we achieved by the end of the quarter:
- A monitoring and notification system: Discord webhooks, Slack webhooks, and email (email notifications were implemented but archived due to budget constraints and the cost of SMTP services)
- User account management: User registration, login, password reset, passwordless authentication via email, and account deletion
- Site-Agnostic Web Scraping: Our web scraping and difference detection works with most web pages without requiring additional programming for each website
- User-friendly Interface: The task dashboard has an intuitive interface for basic task operations (creating, viewing, updating, and deleting tasks).
![WebWatch task_dropdown](https://github.com/user-attachments/assets/8a5aabcf-fab7-48d6-8ce0-fa69050773bb)

**It is best suited for publicly acessible websites that don't implement anti-botting mechanisms. For instance, [course offerings and registration status](https://pisa.ucsc.edu/class_search/), [parking permit availabilities](https://ucsc.aimsparking.com/permits/?cmd=new), portfolios, and job boards.**

## How We Built It
![Diagram showing WebWatch architecture](https://github.com/user-attachments/assets/14b81beb-2126-43d7-ab46-1bd5ba049709)

### Backend
We used Python with [FastAPI](https://fastapi.tiangolo.com/) to build our backend REST API, [SQLite](https://www.sqlite.org/index.html) as our temporary database, and [SQLModel](https://sqlmodel.tiangolo.com/) as our ORM to interact with the database. 
The task scheduler used [AsyncIO](https://docs.python.org/3/library/asyncio.html) for asynchronous job scheduling, and a combination of [Selenium](https://selenium-python.readthedocs.io/), [beautifulsoup4](https://pypi.org/project/beautifulsoup4/), and [difflib](https://docs.python.org/3/library/difflib.html) was used to implement our web scraping and change detection.

### Frontend
Our frontend was built with [React](https://react.dev/) and [Tailwind CSS](https://tailwindcss.com/).

### Infrastructure and DevOps
We deployed WebWatch at https://webwatch.live on an Ubuntu cloud VM using [Traefik](https://doc.traefik.io/traefik/) as our reverse proxy and [nginx](https://nginx.org/en/) for serving our frontend site to Traefik internally. This was orchestrated using [Docker Compose](https://docs.docker.com/compose/). 
We used [Github Actions](https://github.com/features/actions) to create CI/CD pipelines including automated styling checks, API unit tests, and automatic deployment to our live site upon pushing to `main`. During development, we used [DevContainers](https://code.visualstudio.com/docs/devcontainers/create-dev-container) to minimize platform and version conflicts, which also allowed for a smooth transition into deployment.

### Project Management and Agile Framework
We followed the Scrum framework and worked on the project for a duration of 8 weeks, comprised of four two-week sprints. We held Scrum meetings 3 times a week, rotating scrum masters at least once during each sprint. Our scrum documents and other deliverables from the course can be found [here](https://drive.google.com/drive/folders/1JtEnsr-VX9bvBuA7kD7TKDM91VE9bgVL?usp=sharing)

# WebWatch Archival and Alternatives
WebWatch is no longer being developed or hosted for use. As an alternative, we recommend https://changedetection.io/, an established open-source project.

# For Developers: DevContainer Setup/Usage
- Install Dev Container VSCode Extension
    - https://code.visualstudio.com/docs/devcontainers/tutorial
- Open the frontend or backend folder in VSCode.
- Open the project in the Dev Container (through Extension GUI prompt or "Open a Remote Window" icon in the bottom left of VSCode)
- Container will take a moment to copy its image, install project dependencies (requirements.txt for backend, or package.json for frontend) and start.
- Work normally; project file changes are saved to the host machine.
- If you get issues when committing or pushing code, try reopening the project locally to do it from outside the container.

## Python Package Management
- Python packages/versions named in `backend/requirements.txt` are automatically installed via `pip` with container root (no virtual environment).
- If you install new packages, run the following in `backend/` to update `requirements.txt`: 
    - `pip freeze > requirements.txt`

