# Dawai

#### How to use and enter the virtual environment in python:

### for creating a virtual environment:

python -m venv env

### for entering a virtual environment

source env/bin/activate

### How to check if you are using the virtual environment?

see the (env) before the comand line header, for example:
(env) shino@ShinoPC:~/class-demos/company/MVPv2/backend$

### How to initialize the migration file?

### creating a migration file

flask db init

### making the migration version file

flask db migrate

### commiting the changes of the migration version file

flask db upgrade

### undo the changes of the migration version file

flask db downgrade

### to reset the migration file, go to the CLI of DB and write the following command:

DROP TABLE alembic_version;

### master user for database-dawai:

endpoint: database-dawai.cyd5dayxhyym.me-south-1.rds.amazonaws.com
user: postgres
password: Dawai-2000
database: dawai

### IMPORTANT NOTE:

After creating a migration, either manually or as --autogenerate, you must apply it with alembic upgrade head. If you used db.create_all() from a shell, you can use alembic stamp head to indicate that the current state of the database represents the application of all migrations.

YOU can use the following command to make the database up to date:

$ flask db stamp head
$ flask db migrate
$ flask db upgrade
