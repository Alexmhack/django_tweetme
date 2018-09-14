# django_tweetme
Designing Twitter Basic Version Clone In Django, Ajax, Bootstrap and much more

# Django Project Setup
1. Start django project
	```
	django-admin startproject tweetme .
	```

2. Run migrations and create super user
	```
	python manage.py migrate
	python manage.py createsuperuser
	```

3. Run the server
	```
	python manage.py runserver
	```

# Django Project Settings
For production and development django has two different environments and settings so for
production django has to be configured first, that is what we will be doing here.

Create a new folder inside the **tweetme** folder where ```settings.py``` file lies.
Now create **settings** folder a python module by simply creating a ```__init__.py``` file.

Now the real thing starts!

Inside the **settings** folder create three new files namely

```
settings/local.py
settings/base.py
settings/production.py
```

Then open actual ```settings.py``` file and copy the whole code from there and paste it in
each of the above three files that we just created.

Now simply delete the ```settings.py``` file because we won't be using it anymore.

**Changes** that needs to done in the new settings file are 

Inside **production.py** file
```
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ellflv!5zwbvz@a@vt67il@o-sijjea&nh7q*4d6(#zo*v5&zn'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []
```

**Notice** we have one most important change which is changing ```DEBUG = False``` which
seems obvious because of the **warning** given above it.

And one more change is to define our new path which is for all the files inside the 
**settings** folder for ```BASE_DIR``` by simply jumping back one more folder using ```
os.path.dirname``` which does everything.

Okay the last thing is to create a ```.env``` file which will have all the environment
variables like the ```SECRET_KEY```

For that we will be using a python package ```python-dotenv``` install it using

```
pip install python-dotenv
```

Create a file ```.env``` in main folder or where ```manage.py``` file lies and inside that
file put your variable in format

```
SECRET_KEY=YOUR-SECRET-KEY-HERE
```

In the **settings** folder in each file put a small piece of code

```
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")
```

```load_dotenv(find_dotenv())``` finds and loads the env variables from ```.env``` file

One last thing is to import everything from our settings files into the ```__init__.py```
file 

```
from .base import *

from .production import *

try:
	from .local import *
except Exception as e:
	print(e)

```

Since we are currently into local or development stage we will be using only 
```local.py``` file.

If everything goes right you can run the server without any errors.

```
python manage.py runserver

Performing system checks...

System check identified no issues (0 silenced).
September 13, 2018 - 15:31:42
Django version 2.0.7, using settings 'tweetme.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

# Serving Static Files
Checkout the django [docs](https://docs.djangoproject.com/en/2.1/howto/static-files/) for best practises and settings needed for serving static
files.

For local or development stage we won't need a server for static files but 
during production a seperate server is what is highly recommended as django.

Make changes in the ```settings/local.py``` 

```
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static-serve')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static-storage')
]

```

This is much like our templates, where we give django the path to the static and
templates folder where those files actually lies.

After this run the command to collectstatic files 

```
python manage.py collectstatic
```

This will copy all the static files from the django and static-storage folder and
paste them into static-serve. What we are doing here is imitating a actual server 
in the form of static-serve folder that acts as a outside server for serving 
static files.

Run the server again and visit the admin site and everything works fine.

If you want to serve your static files which we will do later on then create that
file in **static-storage** folder and run **collectstatic**

# Tweetme App
Start a new app for project using 

```
python manage.py startapp tweets 
```

This app will completely handle the tweets a user can make. We would want a user to write
a tweet content and also record the date and time when the tweet was made.

For this we need to create some fields inside models

**tweets/models.py**
```
from django.db import models

class Tweet(models.Model):
	content = models.CharField(max_length=140)
	updated = models.DateTimeField(auto_now=True)
	timestamp = models.DateTimeField(auto_now_add=True)

```

We have three fields

1. ```content``` -- CharField with max_length of 140 characters
2. ```updated``` -- DateTimeField that gets changed to current time of editing
3. ```timestamp``` -- DateTimeField that gets stored when object is created

Using the ```max_length``` argument sets limit on max number of chars that a user can enter
and ```auto_now``` set to **True** will change the time of ```updated``` field whenever
the object is edited and saved, that's why that field is named ```updated``` and timestamp
simply stores the date and time of creating the particular object.

Run ```makemigrations``` and ```migrate``` and register the app in admin then run server 
and try creating some tweets.

You can also add a ```__str__``` method for our model.

What is missing is that we don't have a particular user attached with his particular tweets
for that we need the user model and a way to connect.

```
from django.db import models
from django.conf import settings

class Tweet(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	content = models.CharField(max_length=140)
	updated = models.DateTimeField(auto_now=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.content

```

Again we have to ```makemigrations``` and ```migrate```
