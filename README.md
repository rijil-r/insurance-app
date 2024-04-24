
# Insurance Application

## Instructions

Clone the repository.

    $ git clone {url}

    $ cd {project_folder}

Create virtual environment.

    $ python -m venv {venv_folder}

Activate the virtualenv for your project.
    
Install project dependencies:

    $ pip install -r requirements.txt
    
    
Then create migrations and apply migrations:

    $ python manage.py makemigrations

    $ python manage.py migrate
    

You can now run the development server:

    $ python manage.py runserver

Optional: Sample data command

    $ python manage.py add_sample_data

