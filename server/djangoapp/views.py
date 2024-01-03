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
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/7aa8825a-d560-42e5-9f7c-8fbeea4a7ebb/dealership-package/get-dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Create a context dictionary
        context = {'dealership_list': dealerships}
        # Return the render response with the context
        return render(request, 'djangoapp/index.html', context)

# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request, dealer_id):
    context = {}

    # Get reviews for the specific dealer
    url = " https://us-south.functions.appdomain.cloud/api/v1/web/7aa8825a-d560-42e5-9f7c-8fbeea4a7ebb/reviews/reviewget"
    api_key = "your_watson_nlu_api_key"  # Replace with your actual Watson NLU API key
    dealer_reviews = get_dealer_reviews_from_cf(url, dealer_id, api_key)

    # Add reviews to the context
    context['reviews'] = dealer_reviews

    return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
def add_review(request, dealer_id):
    # Cloud function URL for cars
    cars_url = "your-cloud-function-domain/cars/car-get"
    
    # Check if the request method is POST
    if request.method == "POST":
        # Get values from the review form
        content = request.POST.get('content')
        purchase_check = request.POST.get('purchasecheck')
        car_id = request.POST.get('car')
        purchase_date_str = request.POST.get('purchasedate')
        
        # Convert purchase_date to a datetime object
        purchase_date = datetime.strptime(purchase_date_str, "%m/%d/%Y").date()
        
        # Get car details from the car id
        car_url = f"your-cloud-function-domain/cars/car-get/{car_id}"
        car = post_request(car_url)
        
        # Prepare review data
        review_data = {
            "time": datetime.utcnow().isoformat(),
            "name": request.user.username,
            "dealership": dealer_id,
            "review": content,
            "purchase": purchase_date.year if purchase_check else None,
            "car_make": car["make"]["name"],
            "car_model": car["name"],
            "car_year": car["year"],
            "sentiment": None,  # You can update this with Watson NLU sentiment later
        }
        
        # Prepare payload
        json_payload = {"review": review_data}
        
        # Cloud function URL for review post
        review_post_url = "your-cloud-function-domain/reviews/review-post"
        
        # Post the review data
        post_request(review_post_url, json_payload)
        
        # Redirect to the dealer details page
        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
    
    elif request.method == "GET":
        # Query cars with the dealer id to be reviewed
        cars = get_dealer_cars_from_cf(cars_url, dealer_id)
        
        # Append queried cars into context
        context = {'cars': cars, 'dealer_id': dealer_id}
        
        # Render add_review.html
        return render(request, 'djangoapp/add_review.html', context)
    
    else:
        # Handle other HTTP methods (PUT, DELETE, etc.) as needed
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



