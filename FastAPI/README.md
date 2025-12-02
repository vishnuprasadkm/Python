# FastAPI

## Pre-requisite
    # Install FastApi
        -> pip install fastapi
    # Create a Virtual environment to run fastAPI
        <!-- fastapienv is a name given to the virtual env(venv), it can be anything -->
            -> python -m venv <env_name>
    # Active the virtual env    
        <!-- fastapienv is the venv name given when creating a venv -->
            -> <env_name>\Scripts\activate.bat
    # Web server to run fast api
        -> pip install "uvicorn[standard]"
    
    # Deactivate Virtual environment
        -> deactivate

## To run the api
    -> uvicorn <FILE_NAME>:<FASTAPI_VARIABLE_NAME> --port <PORT_NUMBER> --reload (in the project root dir) 
    or
    -> uvicorn <FIE_NAME>:<FASTAPI_VARIABLE_NAME> --reload
    For this project - uvicorn index:app --host 0.0.0.0 --port 8000 --reload

    or with latest fastapi version
    fastapi run <file_name>.py  -> for production mode
    or
    fastapi dev <file_name>.py  -> for dev mode

