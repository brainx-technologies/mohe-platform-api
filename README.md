# README

API for mobile for MOHE platform. 

## Development

- create and activate a python virtualenv

    python -m venv mohe
    source mohe/bin/activate

- check out mohe-platform-core    
- link core module
    
    cd <path to core>
    python setup.py develop

- copy settings.ini and edit the file

    cp <path to core>/etc/settings.ini.template /opt/mohe/etc/mohe_api.ini
    
- run api project

    cd <path to api>
    python manage.py migrate
    python manage.py runserver
