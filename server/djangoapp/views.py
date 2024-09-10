# Uncomment the required imports before adding the code

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from datetime import datetime

from django.http import JsonResponse
from django.contrib.auth import login, authenticate
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from .populate import initiate
from .models import CarMake, CarModel


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
    if request.method == "POST":
        # Get username and password from request body (POST)
        try:
            data = json.loads(request.body)
            username = data.get('userName')
            password = data.get('password')
            
            # Authenticate user with the provided credentials
            user = authenticate(username=username, password=password)
            if user is not None:
                # If user is valid, call login method to log in the current user
                login(request, user)
                return JsonResponse({"userName": username, "status": "Authenticated"})
            else:
                # If credentials are invalid
                return JsonResponse({"status": "Authentication failed"}, status=401)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
    return JsonResponse({"error": "POST request required"}, status=405)

# Create a `logout_request` view to handle sign out request
@csrf_exempt
def logout_request(request):
    if request.method == "GET":
        logout(request)
        return JsonResponse({"status": "success", "message": "Logout successful"})
    return JsonResponse({"error": "GET request required"}, status=405)

# Create a `registration` view to handle sign up request
@csrf_exempt
def registration(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get('userName')
            password = data.get('password')
            first_name = data.get('firstName')
            last_name = data.get('lastName')
            email = data.get('email')

            # Check if the username already exists
            if User.objects.filter(username=username).exists():
                return JsonResponse({"userName": username, "error": "Username already taken"}, status=400)

            # Check if the email already exists
            if User.objects.filter(email=email).exists():
                return JsonResponse({"email": email, "error": "Email already registered"}, status=400)

            # Create a new user
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password, email=email)

            # Log in the newly created user
            login(request, user)

            # Return a JSON response with the username and status
            return JsonResponse({"userName": username, "status": "Authenticated"})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except KeyError as e:
            return JsonResponse({"error": f"Missing field: {e.args[0]}"}, status=400)
    return JsonResponse({"error": "POST request required"}, status=405)

def get_cars(request):
    count = CarMake.objects.filter().count()
    print(count)  # Print the count of CarMake records

    # If no cars exist, you might want to initiate or populate data
    if count == 0:
        initiate()  # Make sure the initiate function is defined somewhere to handle this case

    # Query related car models and makes using select_related for optimization
    car_models = CarModel.objects.select_related('car_make')

    # List to hold car model and make information
    cars = []
    for car_model in car_models:
        cars.append({"CarModel": car_model.name, "CarMake": car_model.car_make.name})

    # Return a JSON response with the car models and makes
    return JsonResponse({"CarModels": cars})


# # Update the `get_dealerships` view to render the index page with
# a list of dealerships
# def get_dealerships(request):
# ...

# Create a `get_dealer_reviews` view to render the reviews of a dealer
# def get_dealer_reviews(request,dealer_id):
# ...

# Create a `get_dealer_details` view to render the dealer details
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request):
# ...
