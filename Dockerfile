# this is an official Python runtime, used as the parent image
FROM python:3.6.5-slim

# set the working directory in the container to /app
WORKDIR /app

# add the current directory to the container as /app
ADD ./app /app

# execute everyone's favorite pip command, pip install -r
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# unblock port 8000 for the Flask app to run on
EXPOSE 8000

# execute the Flask app
# CMD ["python", "app.py"]

ENTRYPOINT ["/usr/local/bin/gunicorn", "-w", "1", "--bind", ":8000", "--access-logfile", "-", "wsgi:application"]
