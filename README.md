
customers
=====

customers is a Django app which is used to serve django tenant details. It is used to create tenants, schemas and doamin urls for respective tenants. :fire:

Quick start
-----------
Install the package `pip install dj-auto-multitenant`.

Now make change in your DATABASE_ENGINE

    DATABASES = {
        'default': {
            'ENGINE': 'django_tenants.postgresql_backend',
            # ..
        }
    }

Add DATABASE_ROUTERS setting, so that the correct apps can be synced, depending on what’s being synced (shared or tenant).

    DATABASE_ROUTERS = (
        'django_tenants.routers.TenantSyncRouter',
    )

Add the middleware django_tenants.middleware.main.TenantMainMiddleware to the top of MIDDLEWARE, so that each request can be set to use the correct schema.

    MIDDLEWARE = (
        'django_tenants.middleware.main.TenantMainMiddleware',
        #...
    )

Now change your INSTALLED APPS settings and seprate your shared apps and tenant apps. Add your `customers` app in SHARED APP.

    SHARED_APPS = (
        'django_tenants',  # mandatory
        'customers', # you must list the app where your tenant model resides in

        'django.contrib.contenttypes',

        # everything below here is optional
        'django.contrib.auth',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.messages',
        'django.contrib.admin',
    )

    TENANT_APPS = (
        # The following Django contrib apps must be in TENANT_APPS
        'django.contrib.contenttypes',

        # your tenant-specific apps

        'myapp.houses',
    )

INSTALLED_APPS = list(SHARED_APPS) + [app for app in TENANT_APPS if app not in SHARED_APPS]


Add: 
    TENANT_MODEL = "customers.Client" # app.Model

    TENANT_DOMAIN_MODEL = "customers.Domain"  # app.Model

    CLOUDAMQP = "<YOUR CLOUDAMQP URL>"

Now migrate customers `python manage.py migrate_schemas --shared`