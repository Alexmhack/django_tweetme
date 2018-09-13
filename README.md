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
