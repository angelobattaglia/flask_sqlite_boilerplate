# Flask-SQLite boilerplate

## How to fire this up

On Windows, it's recommended to use Powershell. In the root directory of this project:

```ps1
python -m venv .env
cd .env\scripts
.\Activate.ps1
```

On linux, through bash or zsh
```shell
python3 -m venv .env
cd .env/bin
source activate
```

Then install all of the libraries required
```ps1
pip install -r requirements.txt
pip list # to list the libraries required
```

This will run the Flask development server with debug mode enabled, allowing you to see detailed error messages and take advantage of features like automatic code reloading when changes are made

```ps1
cd app
flask run --debug
```

If you add any new module to this web app via virtual environment of this project,
just update the requirements.txt

```ps1
pip freeze > requirements.txt
```

As for the db viewer, it's recommended to use the [sqlitebrowser](https://sqlitebrowser.org/)

## Users in the database

There's one user user in the DB 

```csv
email, password
b@t.com, grovestreet
```

## Details

The login and signup system is made so that we're using the email to refer to the user. It is
modular, meaning that we could add a nickname to address the user. But by doing so, it's important
to modify the routes in the app.py named "signup" and "login".


### Table Creation

The creation of the tables is being done in app/table_creation.py
