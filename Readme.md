python -m pip install fastapi "uvicorn[standard]" python-multipart jinja2 pandas joblib



How to run (step-by-step)

Open a terminal and cd into the project folder

        cd /path/to/sih-rbs-main/sih-rbs-main

Create & activate a virtual environment (recommended)
Linux / macOS:

        python -m venv venv
        source venv/bin/activate


Windows (PowerShell):

        python -m venv venv
        .\venv\Scripts\Activate.ps1

Windows (cmd.exe)

        python -m venv venv
        .\venv\Scripts\activate

Install dependencies:

        pip install fastapi "uvicorn[standard]" python-multipart jinja2 pandas joblib

        python setup_db.py

        uvicorn app:app --reload --host 127.0.0.1 --port 8000
        uvicorn app:app --reload --host 127.0.0.1 --port 8000


Signup: http://127.0.0.1:8000/signup

Login: http://127.0.0.1:8000/login

Dashboard: http://127.0.0.1:8000/dashboard/{id}

Transfer: http://127.0.0.1:8000/transfer/{id}
