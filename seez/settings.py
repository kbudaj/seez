from os import environ

import envparse

env = envparse.Env()


DATABASE_URL = environ["DATABASE_URL"]
DEBUG = env("DEBUG", cast=bool, default=False)
