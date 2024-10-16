# Dev Container Setup/Usage
- Intall Dev Container VSCode Extension
    - https://code.visualstudio.com/docs/devcontainers/tutorial
- Open this project in the Dev Container (through Extension GUI prompt or "Open a Remote Window" icon in the bottom left of VSCode)
- Container will take a moment to copy its Debian-based image and start
- Work normally; project file changes are saved to the host machine.

## Python Package Management
- Python packages/versions named in `requirements.txt` are automatically installed via `pip` with container root (no virtual environment).
- If you install new packages, run the following in project root to update `requirements.txt`: 
    - `pip freeze > requirements.txt`

