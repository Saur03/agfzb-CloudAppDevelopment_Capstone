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
from django.http import JsonResponse
from .models import CarDealer
from .restapis import get_dealers_from_cf
from .restapis import get_dealer_reviews_from_cf
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
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        url = "your-cloud-function-domain/reviews/review-get"
        api_key = "your_watson_nlu_api_key"  # Replace with your actual Watson NLU API key

        # Get reviews from the URL
        dealer_reviews = get_dealer_reviews_from_cf(url, dealer_id, api_key)

        # Print details for each review, including sentiment
        for review in dealer_reviews:
            print(f"Review: {review.review}")
            print(f"Sentiment: {review.sentiment}")
            print("-" * 30)

        # Return a response (you can customize this part based on your needs)
        return HttpResponse("Reviews and Sentiments Printed in Console")

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
def add_review(request, dealer_id):
    # Check if the request method is POST
    if request.method == "POST":
        url = "your-cloud-function-domain/reviews/review-post"
        api_key = "your_watson_nlu_api_key"  # Replace with your actual Watson NLU API key

        # Create a dictionary object for the review
        review = {
            "time": datetime.utcnow().isoformat(),
            "name": request.user.username,  # Assuming the username is used as the reviewer's name
            "dealership": dealer_id,
            "review": request.POST.get("review", ""),  # You can customize this based on your form fields
            "purchase": bool(request.POST.get("purchase", False)),  # Example: a checkbox indicating purchase
            # Add other attributes based on your review-post cloud function
        }

        # Create a JSON payload with the review
        json_payload = {"review": review}

        # Make the POST request to add a review
        response = post_request(url, json_payload, dealerId=dealer_id, api_key=api_key)

        # Return the response (you can customize this part based on your needs)
        return HttpResponse(f"Review added successfully! Response: {response}")
    else:
        # Handle other HTTP methods (GET, etc.) as needed
        return HttpResponse("Invalid HTTP method")



        
# get_dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/7aa8825a-d560-42e5-9f7c-8fbeea4a7ebb/dealership-package/get-dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)

