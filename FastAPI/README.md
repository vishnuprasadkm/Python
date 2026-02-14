# FastAPI

    # run -> `pip install -r requirements.txt` to install all required packages

## Pre-requisite

    # Create a Virtual environment to run fastAPI
        <!-- fastapienv is a name given to the virtual env(venv), it can be anything -->
            -> python -m venv <env_name>
    # Active the virtual env
        <!-- fastapienv is the venv name given when creating a venv -->
            # in bash -> source venv/Scripts/activate
            # in powershell -> .\venv\Scripts\Activate.ps1
            # in cmd -> venv\Scripts\activate.bat

    # Install FastApi
        -> pip install fastapi
    # Web server to run fast api
        -> pip install "uvicorn[standard]"

    # Deactivate Virtual environment
        -> deactivate

## To run the api

    # If running the project from parent path, instead of import the files directly import it with relative path, i.e., '''from .package import module'''. If running the project from the same project path normal import will work and relative import will not work

    -> uvicorn <FILE_NAME>:<FASTAPI_VARIABLE_NAME> --port <PORT_NUMBER> --reload (in the project root dir)
    or
    -> uvicorn <FIE_NAME>:<FASTAPI_VARIABLE_NAME> --reload
    For this project - uvicorn main:app --host 0.0.0.0 --port 8000 --reload

    or with latest fastapi version
    fastapi run <file_name>.py  -> for production mode
    or
    fastapi dev <file_name>.py  -> for dev mode

## Import Error

    -> If getting ModuleNotFound Error because of existing file, it may be due to relative import, it can be fixed by import the file from the relative path.
        Example -  '''from abc import xyz -> from .abc import xyz''' **for same level . or one more level .. **
