from .base import *

DEBUG = False
ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS", cast=lambda hosts: [host.strip() for host in hosts.split(",")]
)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASSWORD"),
        "HOST": config("DB_HOST"),
        "PORT": config("DB_PORT"),
    }
}