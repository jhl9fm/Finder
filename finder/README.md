# project-1-22

Installation:
- Clone our Github repo
- Run pip install requirements.txt
- Run python manage.py runserver

App Functionality:
- Log in using your Google account
- Search Events page 
    - Search for specific events by filtering based on event type, COVID safety level, and event date
    - Allow location access to see your location and the location of other events on the map
    - Double click on events that show up in the search to center them on the map and reorder other events by distance
    - Click details to view the information about each event
    - Click register to register for the event using your login information (you will receive an email upon registering)
- Manage Events page: this page displays all the events you have created
    - Create a new event by clicking "Add new"
    - Update or delete event by clicking the icons next to each event
- Registered Events page: this page displays all the event you are registered for
    - Information about each event is displayed
    - Each registered even has a unique, randomly generated confirmation number you can compare with the one sent in the email


References:
https://whizzoe.medium.com/in-5-mins-set-up-google-login-to-sign-up-users-on-django-e71d5c38f5d5
https://docs.djangoproject.com/en/3.1/intro/tutorial01/
https://code.visualstudio.com/docs/python/tutorial-django
https://www.javatpoint.com/django-crud-application
https://django-crispy-forms.readthedocs.io/en/latest/layouts.html

