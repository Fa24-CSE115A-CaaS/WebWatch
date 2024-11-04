# Dev Container Setup/Usage
- Intall Dev Container VSCode Extension
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

