
service_auth
=====

A small package to connect microservices and authenticate user. It uses RemoteModel to make http requests with multiple services.
Also used to verify tokens to authenticate users.

Quick start
-----------
Install the package `pip install dj-micro-auth-connect`.

Add `service_auth` in INSTALLED_APPS

    INSTALLED_APPS = (
        ...
        'service_auth'
    )

Add
    ENTITY_BASE_URL_MAP = {
        ...
    'auth':'url-for-authentication-service.com',
    }

    ENTITY_URL_PATH = {
        ...
    'verify_token':'api/path/for/endpoint',
    }

* Note: Above mentioned keys must be same to get it work.
