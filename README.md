# Unzip package
unzip seez-feat-initial.zip
cd seez-feat-initial

# Build and start docker environment
docker-compose up

# seez-postgres and seez-api should be running now
# On different terminal connect to seez-api
docker exec -it seez-api bash

# In entry point folder (/app/seez) run migration
alembic upgrade head

# After successfull migration, import data
python manage.py import_data

# API should be ready now, but let's run tests to make sure everything is okay
# Go one directory up
cd ..

# Run tests
py.test -vv

# Test validates code style, imports with flake8
# It also validates correct type annotation with mypy.
# Mypy first run might take a couple of seconds.
# Next text executions use cache


# API
API should be available on http://0.0.0.0
FastAPI provides docs on http://0.0.0.0/docs
It describes available params/endpoints but I will describe it as well a bit.

# GET /make/
Returns all makes

# GET /model/
Returns all models

# GET /submodel/
Returns all submodels

# GET /car/
This one is more interesting. There was a lot of data so I decided to implement simple pagination.
Endpoint supports following query params:
- page_number
- page_size
- price_min
- price_max
- mileage_min
- mileage_max
They can be used together like this:

http://0.0.0.0/car/?price_max=10000&price_min=8000&mileage_min=200000&mileage_max=300000&page_number=2


# POST /car/
Adding car. I had to make some logic assumptions here. Normally I would contact you, but I didn't want to bug you with it, since it's just interview excercise.




