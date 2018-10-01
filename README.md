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

One more django provided mixin for authentication is the ```LoginRequiredMixin``` which is
definitely more advanced than our custom mixin

**tweets/views.py**
```
from django.contrib.auth.mixins import LoginRequiredMixin
...

class TweetCreateView(LoginRequiredMixin, FormUserNeededMixin, CreateView):
	form_class = TweetModelForm
	template_name = "tweets/tweet_form.html"
	success_url = "/tweet/tweets"
	login_url = "/admin"
```

Once again if a non-logged in user visits the page the **404 PAGE NOT FOUND** error would
show, that means a user has to be logged in to view the page.

## UpdateView
We will be creating view for updating our tweets, we won't want our users to actually do 
that but for sake of learning we will be doing it.

**tweets/views.py**
```
from django.views.generic import ListView, DetailView, CreateView, UpdateView
...

class TweetUpdateView(UpdateView):
	form_class = TweetModelForm
	template_name = "tweets/update_view.html"
	success_url = "/tweet/tweets"
```

Again a url for a view

```
from .views import (
	TweetDetailView,
	TweetListView,
	TweetCreateView,
	TweetUpdateView,
)

	...
	path('edit/', TweetUpdateView.as_view(), name='edit'),
]
```

Also don't forget to create a template with the same form that exists in 
```detail_view.html```

Run the server and visit 127.0.0.1:8000/tweet/1/edit and the form is displayed with
the content already in the field. Change the content and hit save, we get redirected
to tweets list and our first tweet is changed.

Since we have been following the **DRY** principle from so long, we will implement it
here too

Instead of two html files containing the same form we will have only one add some 
changes in both.

**tweets/tweet_form.html**
```
<form action="" method="POST">

	{% csrf_token %}
	{{ form.as_p }}
	<input type='submit' value="{{ btn_value }}">

</form>
```

And in the other ```create_view.html``` file and ```detail_view.html``` files we need
to include this one

**tweets/create_view.html**
```
{% include "tweets/tweet_form.html" with form=form btn_value="Tweet" %}
```

**tweets/update_view.html**
```
{% include "tweets/tweet_form.html" with form=form btn_value="Tweet" %}
```

And if ```create_view.html``` files doesn't exist, create one and change the template
path for create view

**tweets/views.py**
```
class TweetCreateView(LoginRequiredMixin, FormUserNeededMixin, CreateView):
	form_class = TweetModelForm
	template_name = "tweets/create_view.html"
	success_url = "/tweet/tweets"
	login_url = "/admin"
```

## Update View
Django has class for update view as well.

**tweets/views.py**
```
from django.views.generic import ListView, DetailView, CreateView, UpdateView
...

class TweetUpdateView(LoginRequiredMixin, UpdateView):
	queryset = Tweet.objects.all()
	form_class = TweetModelForm
	template_name = "tweets/update_view.html"
	success_url = "/tweet/tweets"
```

This won't allow anonymous users to edit / update any tweet.

But what will happen there are many users and one user edits other person's tweet. Create
another user from the admin site and make a tweet for that user. Edit that tweet from 
the ```UpdateView``` and hit save. That tweet gets updated and it doesn't even belong to you.

So to stop this behaviour we create another mixin since class based views work with mixins
only.

**tweets/mixins.py**
```
...
class UserTweetMixin(FormUserNeededMixin, object):
	def form_valid(self, form):
		if form.instance.user == self.request.user:
			return super().form_valid(form)
		else:
			form._errors[forms.forms.NON_FIELD_ERRORS] = ErrorList(["You are not allowed to change other's content"])
			return self.form_invalid(form)
```

Import and add this mixin to ```UpdateView```

**tweets/views.py**
```
from .mixins import FormUserNeededMixin, UserTweetMixin
...

class TweetUpdateView(LoginRequiredMixin, UserTweetMixin, UpdateView):
	queryset = Tweet.objects.all()
	form_class = TweetModelForm
	template_name = "tweets/update_view.html"
	success_url = "/tweet/tweets"
```

Now try editing the tweet of other user while you are logged in and it shows the error.

## [Delete View](https://docs.djangoproject.com/en/2.1/ref/class-based-views/generic-editing/#django.views.generic.edit.DeleteView)
Inside views just import 

```
from django.views.generic import (
	ListView,
	DetailView,
	CreateView,
	UpdateView,
	DeleteView
)

...
class TweetDeleteView(LoginRequiredMixin, DeleteView):
	model = Tweet
	success_url = "/tweet/tweets"
```

This is it for views, now as we have did for other views, create a url for this view
as well

**tweets/urls.py**
```
from .views import (
	TweetDetailView,
	TweetListView,
	TweetCreateView,
	TweetUpdateView,
	TweetDeleteView,
)
...

	path('<int:pk>/delete/', TweetDeleteView.as_view(), name='delete'),
]

```

run the server and head to for example 127.0.0.1:8000/tweet/1/delete and you should get
an error saying template does not exist and the template name. This template name and 
location is default which our class-based view uses so simply create a template and 
from the [docs](https://docs.djangoproject.com/en/2.1/ref/class-based-views/generic-editing/#django.views.generic.edit.DeleteView) copy paste the html for this 
template and refresh the page. If you click confirm then the tweet will be deleted from
the database and you will be redirected to the list view and the tweet no longer exists.

# Reverse URLS
```reverse``` and ```reverse_lazy``` are functions that take in the url name and returns
the complete url. Refer to [docs](https://docs.djangoproject.com/en/2.1/ref/urlresolvers/) for more info.

**tweets/views.py**
```
from django.urls import reverse_lazy
...


class TweetDeleteView(LoginRequiredMixin, DeleteView):
	model = Tweet
	success_url = reverse_lazy("tweets:delete")
```

Instead of writing out the complete url we just pass in the namespace and urlconf name
and that's it.

Our model also needs a ```get_absolute_url``` method

**tweets/models.py**
```
from django.urls import reverse

...
	def get_absolute_url(self):
		return reverse('tweets:detail', kwargs={'pk': self.pk})
```

With this implemented we no more need the success_url in update and create view but
we still need it in delete view.

# Search View
So let's start by some requests

In ```tweets/views.py``` add a ```get_queryset``` function in ListView

```
class TweetListView(ListView):
	model = Tweet
	template_name = "tweets/list_view.html"

	def get_queryset(self):
		qs = Tweet.objects.all()
		print(self.request.GET)
		return qs
```

That simply returns all the objects and also prints the request **GET** data onto 
console. This is the lead through which we will make some searches just like we do in
twitter app for other tweets.

So add some more logic
```
	...
	def get_queryset(self):
		qs = Tweet.objects.all()
		query = self.request.GET.get("q", None)
		if query is not None:
			qs.filter(content__icontains=query)
			return qs
		return qs
```

Now just click this [127.0.0.1:8000/tweet/q=content](http://127.0.0.1:8000/tweet/q=content) and you get the results for the search query.

You can make your template show this data in proper way

**templates/tweets/list_view.html**
```
{% include "tweets/search_form.html" %}

{% for obj in object_list %}

	{{ obj.content }}<br>
	{{ obj.timestamp|timesince }}<br>
	{{ obj.user }}<br><br><br>

{% empty %}

	{% if request.GET.q %}
		<h3>No tweets found.</h3>
	{% else %}
		<h3>No tweets yet.</h3>
	{% endif %}

{% endfor %}
```

If you search something that doesn't match anything from the database then you would
get **No tweets found.**

You can also add a search form using a html file

**tweets/search_form.html**
```
<form action="{% url 'tweets:list' %}" method="get" accept-charset="utf-8">
	
	<input type="text" name="q" placeholder="Search">
	<input type="submit" value="Search">

</form>
```

And include this template inside the list view at top since we want search form to be 
at top

**list_view.html**
```
{% include "tweets/search_form.html" %}
...
```

We can go a little more further by doing 

**search_form.html**
```
...
	<input type="text" name="q" placeholder="Search" value="{{ request.GET.q }}">
...
```

This would show the searched value in the search form.

## Advanced Searching With [Q](https://docs.djangoproject.com/en/2.1/topics/db/queries/#complex-lookups-with-q-objects)

Complex lookups will help us in advancing our search form queries.

```
from django.db.models import Q

...
class TweetListView(ListView):
	template_name = "tweets/list_view.html"

	def get_queryset(self):
		qs = Tweet.objects.all()
		query = self.request.GET.get("q", None)
		print(self.request.GET)
		if query is not None:
			qs = qs.filter(
				Q(content__icontains=query) |
				Q(user__username__icontains=query)
			)
		return qs
```

This allows users to search for the username and the tweets related to that user will
be shown in results.

# Redirect View
**tweets/urls.py** file looks like

```
...
urlpatterns = [
	path('<int:pk>/', TweetDetailView.as_view(), name='detail'),
	path('', TweetListView.as_view(), name='list'),
	path('create/', TweetCreateView.as_view(), name='create'),
	path('<int:pk>/edit/', TweetUpdateView.as_view(), name='edit'),
	path('<int:pk>/delete/', TweetDeleteView.as_view(), name='delete'),
]
```

And **tweetme/urls.py** looks like

```
...
from tweets.views import TweetListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TweetListView.as_view(), name='home'),
    path('tweet/', include('tweets.urls', namespace='tweets')),
]
```

So here as you can see we have two urlconfs routing to the same view that is 
```TweetListView``` let's change that.

In **tweets** urls change

```
	path('', TweetListView.as_view(), name='list'),
```

to 

```
	path('search/', TweetListView.as_view(), name='list'),
```

Which means whenever a search takes place from the search form the url for that will
be ```/tweet/search?q=```. Now if you go to [127.0.0.1:8000/tweet](http://127.0.0.1:8000/tweet) you will get **404 PAGE NOT FOUND** error because no
view is associated with that url.

So what I am trying to do is redirect the webpage to ```127.0.0.1:8000/``` whenever
```127.0.0.1:8000/tweet/``` is entered in the browser. And we can make this happen
using django ```RedirectView```

Inside **tweets/urls.py**
```
urlpatterns = [
	path('', RedirectView.as_view(url="/", permanent=True)),
	path('<int:pk>/', TweetDetailView.as_view(), name='detail'),
	path('search/', TweetListView.as_view(), name='list'),
	path('create/', TweetCreateView.as_view(), name='create'),
	path('<int:pk>/edit/', TweetUpdateView.as_view(), name='edit'),
	path('<int:pk>/delete/', TweetDeleteView.as_view(), name='delete'),
]
```

Make changes to url that point to ```TweetListView``` and add a new url which 
redirects to the base url. Visit [docs](https://docs.djangoproject.com/en/2.1/ref/class-based-views/base/#redirectview) for more detail on ```RedirectView```

# Tweet From Home Page
Now we will implement a form on the home page with which users can tweet directly
from the home page where there is list of all tweets.

```
<div class="row">
	<div class="col-md-4 mt-5">
		{% if request.user.is_authenticated and not request.GET.q %}
			<h3 class="p-4 bg-info text-white border-red border border-info">{{ request.user }}</h3>
			<!-- include template with create form -->
			{% include "tweets/tweet_form.html" with form=create_form btn_value="Tweet" action_url=action_url %}
		{% else %}
			<h3 class="btn btn-info">Login</h3>
		{% endif %}
	</div>

	<div class="col-md-8">
		{% for obj in object_list %}
		...
```

We are using the ```tweets/tweet_form.html``` again this time with ```create_form```
and ```btn_value="Tweet"```

Pass the ```create_form``` in the ListView using ```get_context_data``` method

```
class TweetListView(ListView):
	template_name = "tweets/list_view.html"

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		context['create_form'] = TweetModelForm()
		context['action_url'] = reverse_lazy('tweets:create')
		return context
```

We simply pass the ```TweetModelForm()``` with brackets means we are not requesting
any data just showing the form.

And just a little change in ```tweet_form.html``` 

```
<div class="mt-5">
	<form action="{% if action_url %}{{ action_url }}{% endif %}" method="POST">

		{% csrf_token %}
		{{ form.as_p }}
		<button type="submit" class="btn btn-success">{{ btn_value }}</button>

	</form>
</div>
```

Simply check if a variable ```action_url``` exists, if yes then put it in the action
attribute of the form. This way we send our form to the ```create``` form url and a 
new tweet is made.

Now we have a form in the homepage that only renders when user is authenticated and 
also let's user tweet directly.

Run the server and try out the form.

# [Django Crispy Forms](https://django-crispy-forms.readthedocs.io/en/latest/install.html)

A more powerful and easier way to handle forms is by using **django-crispy-forms**

Install the package using

```
pip install --upgrade django-crispy-forms
```

Then add it in ```INSTALLED_APPS``` of **local** and **production** settings and also a template among the available options on the [docs](https://django-crispy-forms.readthedocs.io/en/latest/install.html)

```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'tweets',
]

...
# at the bottom add the bootstrap4 pack
CRISPY_TEMPLATE_PACK = 'bootstrap4'
```

And then in ```tweet_form.html``` file as well as any other form that we render using {{ form.as_p }} or in tabular way we can simply load crispy_form_tags

**tweet_form.html**
```
{% load crispy_forms_tags %}
...
{{ form|crispy }}
```

Try removing the ```attrs``` from **tweets/forms.py** file from the fields and
look at the form again

**NOTE:** This was just a demonstration of how you can use the popular form styling
module for django. It's completely on you to use this package or not.

# Django Test
In this section we will be making use of the ```tests.py``` file that exists in **tweets** app

This file is mainly to test the functionality of our django apps.

```
from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import Tweet

User = get_user_model()

class TweetModelTestCase(TestCase):
	def setUp(self):
		random_user = User.objects.create(username='thisistestuser', password='trydjango')

	def test_tweet_item(self):
		test_obj = Tweet.objects.create(
			user=User.objects.first(),
			content='This is some random test content'
		)

		self.assertTrue(test_obj.content == 'This is some random test content')
```

Above is a very simple test that checks if the content of the tweet object made
is actually equal.

```setUp()``` is the main function in a ```TestCase``` class. This function sets the
environment before testing. In ```setUp()``` method we create a new user and then
while creating a ```Tweet``` object we pass in the first user that exists in the 
database.

So why did I create another user when **superuser** exists already in the database.

This is because **django tests** creates a separate ```alias``` database which exists till the test is completed.

Run the tests using 

```
python manage.py test

Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.
----------------------------------------------------------------------
Ran 1 test in 0.008s

OK
Destroying test database for alias 'default'...
```

This is the output of a correct test. If test fails then it will give errors in
the console and that means your code needs some improvement. Follow the errors on
the console and correct your code accordingly.

You can also run some more tests like

```
...
from django.urls import reverse

from .models import Tweet

User = get_user_model()

class TweetModelTestCase(TestCase):
	def setUp(self):
		random_user = User.objects.create(username='thisistestuser', password='trydjango')

	def test_tweet_item(self):
		test_obj = Tweet.objects.create(
			user=User.objects.first(),
			content='This is some random test content'
		)
		test_obj_url = reverse("tweets:detail", kwargs={'pk': test_obj.id})

		self.assertTrue(test_obj.content == 'This is some random test content')
		self.assertTrue(test_obj.id == 1)
		self.assertEqual(test_obj.get_absolute_url(), test_obj_url)
```

Here we test if the ```id``` of the ```test_obj``` we created is equal to **1** 
because we only have a user which has **id** 1.

Using ```self.assertEqual``` we check if the detail url of ```test_obj``` is equal
to the url we fetch using ```reverse```

There are lots of more test that we can create for our django app. Try out yourself 
by creating tests for any more component for your app.

You can separate the url test by

```
	...
	def test_tweet_url(self):
		test_obj = Tweet.objects.create(
			user=User.objects.first(),
			content='This is some random test content'
		)
		test_obj_url = reverse("tweets:detail", kwargs={'pk': test_obj.id})		
		self.assertEqual(test_obj.get_absolute_url(), test_obj_url)
```

Run the test again and you should get ```Ran 2 tests in 0.018s```

```
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
..
----------------------------------------------------------------------
Ran 2 tests in 0.018s

OK
Destroying test database for alias 'default'...
```

# [Django Rest Framework](http://www.django-rest-framework.org/)
Install the **django-rest-framework** using

```
pip install djangorestframework
pip install markdown       # Markdown support for the browsable API.
pip install django-filter  # Filtering support
```

And add the framework in ```INSTALLED_APPS``` of ```local.py``` settings

```
INSTALLED_APPS = [
    ...
    'rest_framework',
]
```

Then before creating any serializers we will create an **api** module inside **tweets** folder

So create **api** folder in **tweets** app and in that folder create ```__init__.py``` file for making it a python module.

Now create three more files inside **api** folder namely

1. ```views.py```
2. ```serializers.py```
3. ```urls.py```

First we will be implementing urls for rest framework. Add the below code in that 
```api/urls.py```

```
from django.urls import path

urlpatterns = [
	
]
```

Now before adding endpoints for our tweet app api we have to add those endpoints in
project urlconfs

```
	...
    path('tweet/api/', include('tweets.api.urls', namespace='tweets-api')),
]
```

Now we will create our first [serializer](http://www.django-rest-framework.org/api-guide/serializers/#serializers) inside ```serializers.py``` file

```
from rest_framework import serializers

from tweets.models import Tweet

class TweetModelSerializer(serializers.ModelSerializer):
	class Meta:
		model = Tweet
		fields = "__all__"
```

Our serializer will be ```ModelSerializer``` that is based on our ```Tweet``` model
and will include all fields.

Now we have our model serializer ready, we will create a view for it.

**api/views.py**
```
from rest_framework import generics

from tweets.models import Tweet
from .serializers import TweetModelSerializer

class TweetListAPIView(generics.ListAPIView):
	serializer_class = TweetModelSerializer

	def get_queryset(self):
		return Tweet.objects.all()
```

This is so similar to what we do in our **views** We define a model in there, which 
is serializer_class in here and assign our serializer that we just created. Then we
define the queryset for this view which will be all the objects that exists in the 
Tweet model so ```Tweet.objects.all()``` . We are using [ListAPIView](http://www.django-rest-framework.org/api-guide/generic-views/#listapiview) which is 
like the ListView.

Now we define a url endpoint for showing the list of all the objects by

**api/urls.py**
```
from django.urls import path

from .views import TweetListAPIView

urlpatterns = [
	path('', TweetListAPIView, name='list')
]
```

This will be the root url which is [127.0.0.1:8000/tweet/api/](http://127.0.0.1:8000/tweet/api/) 

So run the server and visit the above url. You get the Tweet model objects displayed
in JSON format. But one thing that isn't proper is the key ```user``` which displays
the ```id``` as the value. We want to change that behaviour.

# Accounts App
```python manage.py startapp accounts```

add **accounts** app in ```INSTALLED_APPS```

Again create a **api** folder with the same four files and in ```serializers.py``` file create a serializer for ```user``` model

```
from rest_framework import serializers

from django.contrib.auth import get_user_model

User = get_user_model()

class UserModelSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = [
			'username',
			'first_name',
			'last_name'
		]
```

This is very similar to what we did in the tweet serializer, if you are not familiar
with ```get_user_model``` it just gives us the default user model that exists in 
django.

Our serializer is based on the ```User``` model and for the fields we pass in the 
```username``` ```first_name``` ```last_name``` actually we could have just done
```"__all__"``` but that would give us ```email``` as well which we won't need at 
this stage.

Now that we have a serializer for user model we need to use this serializer in 
tweet serializer model

```
class TweetModelSerializer(serializers.ModelSerializer):
	user = UserModelSerializer()
	
	class Meta:
		model = Tweet
		fields = [
			'user',
			'content'
		]
```

Now simply view this [127.0.0.1:8000/tweet/api/](http://127.0.0.1:8000/tweet/api/)
in your browser and you in the user field you get all additional fields for the user
that are username, first_name, last_name.

Just showing what more rest framework serializers can do is by using a model field

```
class UserModelSerializer(serializers.ModelSerializer):
	follower_count = serializers.SerializerMethodField()

	class Meta:
		model = User
		fields = [
			'username',
			'first_name',
			'last_name',
			'follower_count',
		]

	def get_follower_count(self, obj):
		return 0
```

Above we are making a seperate serializer model field which is as simple as just 
intializing it with ```SerializerMethodField()``` and then including it in **fields**
list. What functionality this new field gives is done using ```get_<field_name>()```

The argument ```obj``` refers to the model of the serializer which in this case is 
```User``` model.

We will get there when we add a follower system but for now we ```return 0```
run server and visit the list api view again and you will find the new field added
to our user model.

# AJAX View
Now that we have our APIs ready we want to use the data that will be returned from 
that api using AJAX.

Inside ```base.html``` file add a block tag for javascript just after we load 
the **jQuery file**

```
	...
	<script type="text/javascript" src="{% static 'js/jquery-3.3.1.min.js' %}"></script>

    <!-- custom script tags -->
    {% block script %}{% endblock %}
    ...
```

Now we will put all our javascript inside these tags. Open ```list_view.html```

```
{% block script %}

<script type="text/javascript">
	$(function() {
		console.log('script is running!!');
	})
{% endblock %}
```

We are logging a message on console when the document loads using jQuery. Run the 
server and visit the url for list view of tweets [127.0.0.1:8000](http://127.0.0.1:8000) and open the developer console.

Now that we have our jQuery running, we can use the ```.ajax``` method to call
our ```/tweet/api``` and request the data

```
{% block script %}

<script type="text/javascript">
	$(function() {
		console.log('script is running!!');

		$.ajax({
			url: "/tweet/api",
			method: "GET",
			success: (data) => {
				console.log(data);
			},
			error: (err) => {
				console.error(err);
			}
		})
	})
</script>

{% endblock %}
```

Open the console again and you will find the array of objects that contains the 
tweet data.

To be more precise we can log the specific data.

```
		$.ajax({
			url: "/tweet/api",
			method: "GET",
			success: (data) => {
				$.each(data, (key, value) => {
					console.log(key);
					console.log(value.user.username);
					console.log(value.content + '\n\n');
				})
			},
			error: (err) => {
				console.error(err);
			}
		})
```

Now we will actually show the tweets using jquery and not by template for loop

```
<div class="row">
	<div class="col-md-8" id="tweet-container">

	</div>

	{% comment %}
	<div class="col-md-8">
		{% for obj in object_list %}

		$.ajax({
			url: "/tweet/api",
			method: "GET",
			success: (data) => {
				$.each(data, (key, value) => {
					var tweetKey = key;
					var tweetUser = value.user.username;
					var tweetContent = value.content;

					$("#tweet-container").append(

						"<div class='card border-dark w-75 mt-4'>" + 
						    "<div class=\"card-body\">" + 
						        "<p class=\"card-text\">" + tweetContent + "</p>" + 
						        "<p class=\"card-text\">via " + tweetUser + "</p>" + 
						        "<a href=\"#\" class=\"btn btn-default\">View</a>" + 
						    "</div>" + 
						"</div>"

					);
				})
			},
			...
```

What we did is comment out the previous data and create a div with same bootstrap 
classes and id of ```tweet-container``` which we use in AJAX.

# Create Form
In this part we will prevent the form to be submitted and call the function to request ajax for tweets list whenever the form is submitted.

Wrap the ajax request in a function
```
function fetchTweets() {
			$.ajax({
				url: "/tweet/api/",
				data: {
					'q': query
				},
				method: "GET",
				success: (data) => {
					tweetList = data;
					parseTweets();
					console.log('fetching tweets is working alright...')
				},
				error: (err) => {
					console.error(err);
				}
			})
		}
```

Now add another attribute to ```tweet_form.html``` 

```
<div class="mt-5">
	<form {% if form_id %}id="{{ form_id }}"{% endif %} action="{% if action_url %}{{ action_url }}{% endif %}" method="POST">
```

Now add ```form_id``` in ```{% include  %}```

```
{% include "tweets/tweet_form.html" with form=create_form btn_value="Tweet" form_id="create-form" %}
```

Then use this **id** of form to handle submit event.

```
	fetchTweets();

	$("#create-form").submit((e) => {
		e.preventDefault();
		console.log(e);
		console.log($(this));
		fetchTweets();
	})
```

Look how we called the ```fetchTweets``` function when document loads and again 
inside the form submit event.
