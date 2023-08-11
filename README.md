    Create a RESTFUL flask application using json data format.
    Use CRUD for endpoints.

    Endpoints are
    /login
    /logout
    /user/list
    /user/create
    /user/delete/{id}
    /user/update/{id}
    /onlineusers

    Data
    /user/create
    {
     "username": "",
     "firstname": "",
     "middlename": "",
     "lastname": "",
     "birthdate": "",
     "email": "",
     "password": ""
    }
    /onlineusers
    {
     "username": "",
     "ipaddress": "",
     "logindatetime": ""
    }
    Store data in postgresql.
    Password should be store salted with sha256.
    Password complexity should be least [A-Za-z0-9] and min 8 characters.
    Data should be validates. Example: email format.
    Log all activities.
    Serve application using uwsgi and nginx.
    Use sqlalchemy for db crud implementation