# BuyThings
#### Video Demo:  <https://youtu.be/cSogmIt-Q3o>
#### Description: BuyThings is a website that you can buy and sell stuff.
#### BuyThings made by using Django framework and sqlite
#### File structure: 
    -buythings*
        -accounts
        -base
        -buythings**
        -cart
        -media
        db.sqlite3
        manage.py
        README.md
##### Buythings* is the parent folder that holds all the files that is necessary for the website
##### Accounts is the django application that handles signup and login actions
In accounts app there is a folder called templates and files called urls.py, views.py. There are bunch of other
files to, but we don't need to get those because this is a basic application. In templates folder there is another folder called accounts. In accounts folder there are two files called registration.html and signup.html.
These files are html templates that shown on website when requested. signup.html:
        
        {% extends 'base.html' %}

        {%  block content %}
            <h2>Sign up</h2>
            <form method="post" autocomplete="off">
                {% csrf_token %}
                {{ form.as_p }}
                <button type="submit">Sign up</button>
            </form>
        {% endblock %}
    
registration.html:

        {% extends 'base.html' %}
    
        {% block content %}
        
            {% load crispy_forms_tags %}
        
            <h2>Log In</h2>
        
        <form method="post" >
            {% csrf_token %}
            {{ login_form|crispy }}
            <button type="submit">Log In</button>
        </form>
        
        {% endblock %}

In urls.py file there are url paths that guides users to needed view. urls.py:

        from django.urls import path

        from . import views
        
        urlpatterns = [
            path('signup/', views.signup, name='signup'),
            path('login/', views.login_request, name='login'),
        ]

views.py file is the where most of the things handled. If a user want ta access a page this request first goes to urls.py file and after that needed
view is getting called. When a view called, view makes preparations and returns needed information which might be
a template and some information for that template to present. views.py:

        from django.shortcuts import render, redirect
        from django.contrib.auth.forms import UserCreationForm
        from django.contrib.auth import login, authenticate
        from django.contrib.auth.forms import AuthenticationForm
        from django.contrib import messages
        
        
        def signup(request):
            if request.method == 'POST':
                form = UserCreationForm(request.POST)
                if form.is_valid():
                    user = form.save()
                    username = form.cleaned_data.get('username')
                    raw_password = form.cleaned_data.get('password1')
                    user = authenticate(username=username, password=raw_password)
                    if user is not None:
                        login(request, user)
                        return redirect('index')
            else:
                form = UserCreationForm()
            return render(request, 'accounts/signup.html', {'form': form})
        
        def login_request(request):
            if request.method == 'POST':
                form = AuthenticationForm(request, data=request.POST)
                if form.is_valid():
                    username = form.cleaned_data.get('username')
                    password = form.cleaned_data.get('password')
                    user = authenticate(username=username, password=password)
                    if user is not None:
                        login(request, user)
                        messages.info(request, f'You are now logged in as {username}')
                        return redirect('index')
                    else:
                        messages.error(request, 'Invalid username ır password')
                else:
                    messages.error(request, 'Invalid username or password')
            form = AuthenticationForm()
            return render(request=request, template_name='accounts/registration.html', context={'login_form':form})

##### Base is the application that handles most of the things and there are templates in it for other applications to inherit from.
In base folder there is a directory called templates which acts exactly the same as the templates folder which in the accounts app but unlike 
accounts/templates directory base/templates directory contains base for other applications to inherit from. Just like accounts/views.py and accounts/urls.py file there are base/urls.py and
base/views.py file that does the exact same things. views.py:

        from django.contrib.auth import logout
        from django.shortcuts import render, get_object_or_404, redirect
        
        from .forms import CommentForm, ProductForm
        from .models import Product, Category, Comment
        
        
        def index(request):
            products = Product.objects.all()
            return render(request, 'base/index.html', {'products': products})
        
        def categories(request):
            category_list = Category.objects.all()
            return render(request, 'base/categories.html', {'categories': category_list})
        
        def product_list(request, pk):
            category = get_object_or_404(Category, pk=pk)
            products = Product.objects.filter(category=category)
            return render(request, 'base/product_list.html', {'category': category, 'products': products})
        
        def details(request, pk):
            product = get_object_or_404(Product, id=pk)
            comments = Comment.objects.filter(commented_product=product)
            form = CommentForm()
        
            if request.method == 'POST':
                form = CommentForm(request.POST)
                if form.is_valid():
                    comment = form.save(commit=False)
                    comment.commented_product = product
                    comment.commentator = request.user
                    comment.save()
                    form = CommentForm()
        
            context = {
                'product': product,
                'comments': comments,
                'form': form,
            }
        
            return render(request, 'base/details.html', context)
        
        def search(request):
            query = request.GET.get('q')
            if query:
                results = Product.objects.filter(name__icontains=query)
            else:
                results = []
            return render(request, 'base/search.html', {'products': results})
        
        def logout_view(request):
            logout(request)
            return redirect('index')
        
        
        def add_product(request):
            if request.method == 'POST':
                form = ProductForm(request.POST, request.FILES)
                if form.is_valid():
                    product = form.save(commit=False)
                    product.seller = request.user
                    product.active = True
                    product.save()
                    return redirect('index')
            else:
                form = ProductForm()
            return render(request, 'base/sell_stuff.html', {'form': form})
        
        
        def my_stuff(request):
            products = Product.objects.filter(seller=request.user)
            return render(request, 'base/my_stuff.html', {'products': products})
        
        
        def remove_my_stuff(request, pk):
            Product.objects.get(id=pk).delete()
            return redirect('my_stuff')

urls.py:
        
        from django.urls import path

        from . import views
        
        urlpatterns = [
            path('', views.index, name='index'),
            path('details/<int:pk>/', views.details, name='details'),
            path('search/', views.search, name='search'),
            path('categories/', views.categories, name='categories'),
            path('categories/<int:pk>/', views.product_list, name='product_list'),
            path('logout/', views.logout_view, name='logout'),
            path('sell_stuff/', views.add_product, name='sell_stuff'),
            path('my_stuff/', views.my_stuff, name='my_stuff'),
            path('remove_my_stuff/<int:pk>/', views.remove_my_stuff, name='remove_my_stuff'),
        ]

There is also a important file called models.py which contains our models that needed in this project.
Models are the database side of the project. When you define a class in models.py and migrate those changes,
django automatically turns that class into sql table. models.py:

        from django.db import models
        from django.contrib.auth.models import User, AbstractUser
        
        
        class Category(models.Model):
            name = models.CharField(max_length=50, default="null")
            def __str__(self):
                return self.name
        class Product(models.Model):
            name = models.CharField(max_length=50)
            description = models.CharField(max_length=200)
            price = models.IntegerField(default=0)
            active = models.BooleanField(default=True)
            seller = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
            contact_number = models.CharField(max_length=12, default='')
            category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
            image = models.ImageField(upload_to='products/', null=True, blank=True)
        
            def __str__(self):
                return self.name
        
        class Comment(models.Model):
            text = models.TextField(default='')
            commented_product = models.ForeignKey(Product, on_delete=models.CASCADE)
            commentator = models.ForeignKey(User, on_delete=models.CASCADE)
            def __str__(self):
                return self.text
        
        class CartItem(models.Model):
            product = models.ForeignKey(Product, on_delete=models.CASCADE)
            user = models.ForeignKey(User, on_delete=models.CASCADE)
        
            def __str__(self):
                return self.product.name

forms.py file contains form templates to display on html files. This way you dont need to write same form again and again. forms.py:

        from django import forms
        from .models import Comment, Product
        
        class CommentForm(forms.ModelForm):
            class Meta:
                model = Comment
                fields = ['text']
        
        class ProductForm(forms.ModelForm):
            class Meta:
                model = Product
                fields = ['name', 'description', 'price', 'contact_number', 'category', 'image']

##### Buythings** is the project file which contains main settings and urls
In buythings** file there is settings.py and urls.py file thats are essential to our project. settings.py:


        """
        Django settings for buythings project.
        
        Generated by 'django-admin startproject' using Django 4.1.5.
        
        For more information on this file, see
        https://docs.djangoproject.com/en/4.1/topics/settings/
        
        For the full list of settings and their values, see
        https://docs.djangoproject.com/en/4.1/ref/settings/
        """
        import os
        from pathlib import Path
        
        # Build paths inside the project like this: BASE_DIR / 'subdir'.
        BASE_DIR = Path(__file__).resolve().parent.parent
        
        
        # Quick-start development settings - unsuitable for production
        # See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/
        
        # SECURITY WARNING: keep the secret key used in production secret!
        SECRET_KEY = 'django-insecure-3f9b84)+*qqsg79(*8y@)+!#59^m-=o!$h9(884@s*+=6l@fa&'
        
        # SECURITY WARNING: don't run with debug turned on in production!
        DEBUG = True
        
        ALLOWED_HOSTS = []
        
        
        # Application definition
        
        INSTALLED_APPS = [
            'base.apps.BaseConfig',
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'crispy_forms',
            'accounts',
            'cart',
        ]
        
        MIDDLEWARE = [
            'django.middleware.security.SecurityMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
        ]
        
        ROOT_URLCONF = 'buythings.urls'
        
        TEMPLATES = [
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': [],
                'APP_DIRS': True,
                'OPTIONS': {
                    'context_processors': [
                        'django.template.context_processors.debug',
                        'django.template.context_processors.request',
                        'django.contrib.auth.context_processors.auth',
                        'django.contrib.messages.context_processors.messages',
                    ],
                },
            },
        ]
        
        WSGI_APPLICATION = 'buythings.wsgi.application'
        
        
        # Database
        # https://docs.djangoproject.com/en/4.1/ref/settings/#databases
        
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }
        
        
        # Password validation
        # https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators
        
        AUTH_PASSWORD_VALIDATORS = [
            {
                'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
            },
            {
                'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
            },
            {
                'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
            },
            {
                'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
            },
        ]
        
        
        # Internationalization
        # https://docs.djangoproject.com/en/4.1/topics/i18n/
        
        LANGUAGE_CODE = 'en-us'
        
        TIME_ZONE = 'UTC'
        
        USE_I18N = True
        
        USE_TZ = True
        
        
        # Static files (CSS, JavaScript, Images)
        # https://docs.djangoproject.com/en/4.1/howto/static-files/
        
        STATIC_URL = 'static/'
        
        # Default primary key field type
        # https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field
        
        DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
        
        LOGIN_REDIRECT_URL = '/'
        
        MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
        
        MEDIA_URL = '/media/'

For example if we want to change base directory of images of our products, we need to change it in hear.
urls.py file is the main url file. Other urls.py files that we talked about are refers to this file. urls.py:

        from django.contrib import admin
        from django.urls import path, include
        from django.conf import settings
        from django.conf.urls.static import static
        
        urlpatterns = [
            path('admin/', admin.site.urls),
            path('accounts/', include('accounts.urls')),
            path('accounts/', include('django.contrib.auth.urls')),
            path('cart/', include('cart.urls')),
            path('', include('base.urls')),
        ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

##### Cart directory is the application handles the cart actions like adding a product to the cart or deleting it.
cart application works exactly like any other application. There is urls.py, views.py files and templates directory.
        
    -cart
        -migrations
        -templates
        -__init__.py
        -admin.py
        -apps.py
        -models.py
        -test.py
        -urls.py
        -views.py

##### Media directory is the file that contains media that need to stored for our models. This might be handled by using thirt party web apps but this project is not at the level of publication so we dont need to use them.

    -media
        -products
            ...

#### Manage.py file is the action handler. If we want to create a new app or run development server we need to use this file.