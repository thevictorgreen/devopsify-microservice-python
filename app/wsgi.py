# wsgi.py
from app import create_app

application = create_app()

if __name__ == "__main__":
    application.run()

# To Serve With Gunicorn WSGI
# gunicorn -w 4 --bind 0.0.0.0 --access-logfile - wsgi:application
