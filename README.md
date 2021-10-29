
service_auth
=====

customers is a Django app which is used to serve django tenant details. It is used to create tenants, schemas and doamin urls for respective tenants. :fire:

Quick start
-----------
Install the package `pip install dj-micro-auth-connect`.

Add `service_auth` in INSTALLED_APPS

    INSTALLED_APPS = (
        ...
        'service_auth'
    )

Add: 
    ENTITY_BASE_URL_MAP = {
        ...
    'auth':'url-for-authentication-service.com',
    }

    ENTITY_URL_PATH = {
        ...
    'verify_token':'api/path/for/endpoint',
    }

* Note: Above mentioned keys must be same to get it work.
