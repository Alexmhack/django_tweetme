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
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	content = models.CharField(max_length=140)
	updated = models.DateTimeField(auto_now=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.content

```

Again we have to ```makemigrations``` and ```migrate```

```on_delete=models.CASCADE``` is for those cases when a user is deleted so django will
delete all the tweet objects related to that user.

# Tweets Views
So we have our model ready for tweets app, now we will create some basic views and then
proceed to more functional views

In the **tweets/views.py** file define a function

```
from django.shortcuts import render

def tweet_detail_view(request, id=None):
	return render(request, 'tweets/detail_view.html', context)

```

**NOTE:** We will be advancing our project to use [class based views](https://docs.djangoproject.com/en/2.1/topics/class-based-views/) but for now we will be 
using [function based views](https://docs.djangoproject.com/en/2.1/topics/http/views/)

If you haven't completed my other tutorials on my [github](https://github.com/alexmhack) 
page please go through them first because I won't be going over all the basics again.

Now create a new file ```tweets/urls.py``` and add in the url for our view

```
from django.urls import path

from .views import (
	tweet_detail_view,
)

app_name = 'tweets'

urlpatterns = [
	path('<int:id>/', tweet_detail_view, name='detail'),
]

```

Notice that we have imported our view and also we have a id argument in our url, we also
have given our url a name and app_name value.

Now simply include the urls for tweets app in the main urls for project

**tweetme/urls.py**
```
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tweet/', include('tweets.urls', namespace='tweets')),
]

```

**NOTE:** We provide the ```namespace``` and ```app_name``` values same

Similarly create a view and its url for listing out all tweets also modify the view to 
actually render the data from database.

**tweets/views.py**
```
from django.shortcuts import render

from .models import Tweet

def tweet_detail_view(request, id=None):
	object = Tweet.objects.get(id=id)
	context = {
		'object': object
	}

	return render(request, 'tweets/detail_view.html', context)


def tweet_list_view(request):
	objects = Tweet.objects.all()
	context = {
		'objects': objects
	}

	return render(request, 'tweets/list_view.html', context)

```

And your ```tweets/urls.py``` file should look like

```
from django.urls import path

from .views import (
	tweet_detail_view,
	tweet_list_view,
)

app_name = 'tweets'

urlpatterns = [
	path('<int:id>/', tweet_detail_view, name='detail'),
	path('tweets/', tweet_list_view, name='tweets'),
]

```

We have given the path for templates but we don't have our templates yet. Create a new 
folder inside **tweets** folder and create files ```list_view.html``` and 
```detail_view.html``` leave them empty for now.

Run the server and go to the urls for list and detail view and you should see a blank 
webpage.

For showing the actual content on the templates simply use the django template tags

**list_view.html**
```
{% for obj in objects %}

	{{ obj.content }}<br>
	{{ obj.timestamp|timesince }}<br><br>

{% endfor %}
```

**detail_view.html**
```
{{ object.content }}<br>
{{ object.timestamp|timesince }}<br>
```

Refresh the page and data shows up

# Class-Based Views
Class Based view removes all the hassle like ```context``` ```return render``` ```request```
```id``` etcetera.

Just import the classes and inherit from them

```
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Tweet

class TweetDetailView(DetailView):
	model = Tweet
	template_name = "tweets/detail_view.html"


class TweetListView(ListView):
	model = Tweet
	template_name = "tweets/list_view.html"
```

```model``` is assigned to the model class ```Tweet``` and ```template_name``` takes the
path for the template because class based view renders default templates.

Configuring urls is as simple as

```
from django.urls import path

from .views import (
	TweetDetailView,
	TweetListView,
)

app_name = 'tweets'

urlpatterns = [
	path('<int:pk>/', TweetDetailView.as_view(), name='detail'),
	path('tweets/', TweetListView.as_view(), name='tweets'),
]
```

**NOTE:** We use ```pk``` in
```path('<int:pk>/', TweetDetailView.as_view(), name='detail'),``` instead of ```id``` 
because class based view requires either ```pk``` or ```slug```

# Django Model Forms
Create a new file ```forms.py``` inside tweets app and in there import the django.forms
and Tweet model

```
from django import forms

from .models import Tweet

class TweetModelForm(forms.ModelForm):
	class Meta:
		model = Tweet
		fields = ("content",)
		exclude = ("user",)
```

What we are doing is creating a ```ModelForm``` with ```Tweet``` model. ```fields``` or
```exclude``` are required for ModelForm to work, excluded fields won't appear in the form
and ```fields = "__all__"``` would show all fields.

Now we need to give django our model form so that it can use our form instead of the default
In ```tweets/admin.py``` file start with some imports

```
from django.contrib import admin

from .models import Tweet
from .forms import TweetModelForm

# admin.site.register(Tweet)

class TweetModelAdmin(admin.ModelAdmin):
	form = TweetModelForm
	# class Meta:
	# 	model = Tweet


admin.site.register(Tweet, TweetModelAdmin)
```

The reason I have commented the ```class Meta:``` because with that our custom form won't
work.

## Custom Validation
Okay! We have our custom form in the admin site but it what our form lacks is custom form
validation. We will look at an example related to our tweet app context

```
from django import forms

from .models import Tweet

class TweetModelForm(forms.ModelForm):
	class Meta:
		model = Tweet
		fields = "__all__"
		# exclude = ("user",)

	def clean_content(self):
		data = self.cleaned_data["content"]
		if "fuck" in data:
			raise forms.ValidationError("Cannot have offensive content")

		return data
```

```clean_content``` the name of the function is actually named this way so that ModelForm
knows that this function is for cleaning ```content``` field.

We simply fetch the data in ```content``` field from the cleaned_data and check if the 
offensive word "fuck" lies in the data itself, if yes then we raise the ValidationError
otherwise we return the data. According to [docs](https://docs.djangoproject.com/en/2.1/ref/forms/validation/)

```
# Always return a value to use as the new cleaned data, even if
# this method didn't change it.
```

Now go to admin site and try to create a tweet and in the content field add the offensive 
word and click save, you will get an error. This way you can add more form validation.

One more way to accomplish the same offensive validation is to define a custom clean method
inside the model itself

**tweets/models.py**
```
class Tweet(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	content = models.CharField(max_length=140)
	updated = models.DateTimeField(auto_now=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.content

	def clean(self, *args, **kwargs):
		content = self.content
		if "fuck" in content:
			raise ValidationError("Cannot have offensive content")

		return super().clean()
```

**Comment** out the ```clean_content``` function inside forms.py

Try creating the tweet with offensive content and the same error again but this time
with the whole object not above the field.

One more similar way is to create a validation function outside the model but add it as 
valiadator to the field

**tweets/models.py**
```
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

def validate_content(value):
	content = value
	if "fuck" in content:
		raise ValidationError("Cannot have offensive content")

	return value


class Tweet(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	content = models.CharField(max_length=140, validators=[validate_content])
	updated = models.DateTimeField(auto_now=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.content
```

**Notice** how we ```validators``` argument in CharField takes a list of validator functions

But having the validator function inside the ```models.py``` file is not recommended way, 
the validators go inside their seperate file

create file ```validators.py``` inside **tweets** app
```
from django.core.exceptions import ValidationError

def validate_content(value):
	content = value
	if "fuck" in content:
		raise ValidationError("Cannot have offensive content")

	return value
```

And inside ```models.py``` just import the validator

```
from django.db import models
from django.conf import settings

from .validators import validate_content
...
```

And we are done.

# Django Views
Along with ```DetailView``` and ```ListView``` django also provides a ```CreateView```
which lets user create an object of the model passed to the ```CreateView``` class

But before that we need to remove the ```user``` field from the ```TweetModelForm``` since
we wouldn't want any user to select the user from options.

**tweets/forms.py**
```
from django import forms

from .models import Tweet

class TweetModelForm(forms.ModelForm):
	class Meta:
		model = Tweet
		fields = ("content",)
		exclude = ("user",)
```

This also needs to be done with the admin site

```
from django.contrib import admin

from .models import Tweet
from .forms import TweetModelForm

# admin.site.register(Tweet)

class TweetModelAdmin(admin.ModelAdmin):
	class Meta:
		model = Tweet
		

admin.site.register(Tweet, TweetModelAdmin)
```

Now the create view

**tweets/views.py**
```
from django.views.generic import ListView, DetailView, CreateView

...
class TweetCreateView(CreateView):
	form_class = TweetModelForm
	template_name = "tweets/tweet_form.html"
	success_url = "/tweet/tweets"

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)
```

Step by step

1. ```form_class``` comes from the [docs](https://docs.djangoproject.com/en/2.1/topics/class-based-views/generic-editing/) which renders the form that we provide with our own
validators

2. ```template_name``` is to tell django the path of the template for the view.

3. ```success_url``` is the url at which the page will be redirected to when form is submitted

4. ```form_valid``` This method is called when valid form data has been POSTed and in there
we simply set the user field of the user with the user who is currently filling the form.

Since we are not assigning model for ```CreateView``` we need to define other details like
```success_url``` and ```template_name``` and ```form_class```

# User Authentication
If you open a private window in your browser and go the [url](http://127.0.0.1:8000/tweet/create/) for create view and try saving a tweet then you will get another error saying
cannot assign anonymous user instance to user id. This error is caused due to no user being
logged into the browser in private window. You will get the same error if you go to admin
site and logout.

For correcting this error we don't want any non-logged user to visit or save the create form

**tweets/views.py**
```
class TweetCreateView(CreateView):
	form_class = TweetModelForm
	template_name = "tweets/tweet_form.html"
	success_url = "/tweet/tweets"

	def form_valid(self, form):
		if self.request.user.is_authenticated:
			form.instance.user = self.request.user
			return super().form_valid(form)
		else:
			return self.form_invalid(form)
```

Class-Based views already have ```form_valid``` and ```form_invalid``` methods so we can
use them here. Using a if statement check if the user is authenticated by checking the 
request object, if yes then execute the below code else make the form invalid which will
stop the functioning of the form.

Try creating tweet with logged out browser window and the form will not redirect which it 
would if user is logged in. But what we lack here is there are no errors in here.

For showing errors we dive into some more advanced django concepts

**tweets/views.py**
```
from django import forms
from django.forms.utils import ErrorList
...

class TweetCreateView(CreateView):
	form_class = TweetModelForm
	template_name = "tweets/tweet_form.html"
	success_url = "/tweet/tweets"

	def form_valid(self, form):
		if self.request.user.is_authenticated:
			form.instance.user = self.request.user
			return super().form_valid(form)
		else:
			form._errors[forms.forms.NON_FIELD_ERRORS] = ErrorList(["User must be logged in to continue"])
			return self.form_invalid(form)
```

Try it out again and you will get errors displayed.

A more clean way would be to create a separate file which would work as [mixin](https://docs.djangoproject.com/en/2.1/topics/class-based-views/mixins/)

Create a file ```tweets/mixins.py```
```
from django import forms
from django.forms.utils import ErrorList

class FormUserNeededMixin(object):
	def form_valid(self, form):
		if self.request.user.is_authenticated:
			form.instance.user = self.request.user
			return super().form_valid(form)
		else:
			form._errors[forms.forms.NON_FIELD_ERRORS] = ErrorList(["User must be logged in to continue"])
			return self.form_invalid(form)
```

What we did is just cut and paste the ```form_valid``` function from ```views.py``` and
just import our mixin ```FormUserNeededMixin``` in there.

**tweets/views.py**
```
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView

from .models import Tweet
from .forms import TweetModelForm
from .mixins import FormUserNeededMixin

class TweetDetailView(DetailView):
	model = Tweet
	template_name = "tweets/detail_view.html"


class TweetListView(ListView):
	model = Tweet
	template_name = "tweets/list_view.html"


class TweetCreateView(FormUserNeededMixin, CreateView):
	form_class = TweetModelForm
	template_name = "tweets/tweet_form.html"
	success_url = "/tweet/tweets"
```

**NOTICE** that we placed ```FormUserNeededMixin``` before ```CreateView```

Our views are a lot cleaner now and everything works just as before
