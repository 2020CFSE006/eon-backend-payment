FROM python:3.6-slim

# Create a user gunicorn so that we don't have to use root user
# We switch to gunicorn user at the bottom of this script
RUN groupadd --gid 1000 gunicorn \
  && useradd --uid 1000 --gid gunicorn --shell /bin/bash --create-home gunicorn

# This forces python to not buffer output / error
ENV PYTHONUNBUFFERED 1

# This is where we will copy all our code
# Workdir creates the directory if it doesn't exist
RUN mkdir /code
WORKDIR /code

# This installs libpq5, which is the postgres native driver
# This is needed later when we install psycopg2
# -------------------------------------------

# Now copy requirements.txt and install all dependencies
# As a best practice, you should pin down version numbers in requirements.txt
#RUN apt-get update -y && apt-get upgrade python-pip -y
RUN python --version
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the remaining code
# Avoid copying the current working directory, 
# as that will have unnecessary files
COPY manage.py .
COPY payment payment 
COPY eon_payment eon_payment
COPY utils utils

# Generate static files
# Note that we pass a dummy secret key
# This secret key is not used when the server is actually started

# Switch to gunicorn user
# This makes our container a lot more secure
#USER gunicorn

# Declare some default values
# These can be overidden when the container is run
ENV PORT 8000
ENV NUM_WORKERS 4
ENV LOG_LEVEL ERROR
ENV DEBUG False

# Start gunicorn with the following configuration
# - Number of workers and port can be overridden via environment variables
# - All logs are to stdout / stderr
# - Access log format is modified to include %(L)s - which is the request time in decimal seconds
#CMD python3 manage.py runserver
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
