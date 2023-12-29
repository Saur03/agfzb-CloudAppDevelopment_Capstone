from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
def static_template_view(request):
    return render(request, 'djangoapp/static_template.html')

# Create an `about` view to render a static about page
def about_us_view(request):
    return render(request, 'djangoapp/about.html')
# def about(request):
# ...


# Create a `contact` view to return a static contact page
def contact_us_view(request):
    return render(request, 'djangoapp/contact.html')

# Create a `login_request` view to handle sign in request
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully logged in.')
            return redirect('index')  # Replace 'index' with the name of your home page URL
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'djangoapp/index.html') 
# ...

# Create a `logout_request` view to handle sign out request
def logout_view(request):
    logout(request)
    messages.success(request, 'Successfully logged out.')
    return redirect('index')
# ...

# Create a `registration_request` view to handle sign up request
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')  # Redirect to the desired page after signup
    else:
        form = UserCreationForm()
    
    return render(request, 'djangoapp/registration.html', {'form': form})
# ...

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

