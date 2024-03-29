# Team 19 CMT313 Spring

This is the repository for our Automated Assessment Tool. The code for this has
been written using **Flask** to create a website.

## Installing

To run the code, first create a virtual environment and install all the packages
from `requirements.txt` using pip. Next, activate your virtual environment. You 
may next want to create a .env file to specify any environment variables. Thirdly,
enable your virtual environment. Finally, use Python to run wsgi.py.

An example using pipenv:
```
pipenv install
pipenv shell
python wsgi.py
```

## AAT Prototype Features Responsibilities

- Question Type 1 (fill in the blank) - Jack
- Question Type 2 (muiliple choice) - Jake
- Formative Assessment - Sam
- Summative Assessment - Chris
- Teaching Staff Review Statistics - Tim

## Usage

The following environment variables can be set:
- ADMIN_PASSWORD
    Specify a password for a default admin account. Username is always "admin", default password is "admin".
- DATABASE_URI
    The path to the database, default uses SQLite.
- SECRET_KEY
    Set a secret key, default is "development".
