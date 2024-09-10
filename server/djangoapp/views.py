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
from .restapis import get_request, analyze_review_sentiments, post_review


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


#Update the `get_dealerships` render list of dealerships all by default, particular state if state is passed
def get_dealerships(request, state="All"):
    if(state == "All"):
        endpoint = "/fetchDealers"
    else:
        endpoint = "/fetchDealers/"+state
    dealerships = get_request(endpoint)
    return JsonResponse({"status":200,"dealers":dealerships})

def get_dealer_reviews(request, dealer_id):
    # Check if dealer_id has been provided
    if dealer_id:
        # Construct the endpoint to fetch reviews for the dealer
        endpoint = f"/fetchReviews/dealer/{dealer_id}"
        # Fetch the reviews using get_request function
        reviews = get_request(endpoint)

        # Loop through each review and analyze the sentiment
        for review_detail in reviews:
            # Analyze the sentiment of each review
            response = analyze_review_sentiments(review_detail['review'])
            # Set the sentiment in the review_detail dictionary
            review_detail['sentiment'] = response.get('sentiment', 'neutral')  # default to neutral if not found

        # Return the reviews along with their sentiment as a JSON response
        return JsonResponse({"status": 200, "reviews": reviews})
    else:
        # If dealer_id is not provided, return a bad request status
        return JsonResponse({"status": 400, "message": "Bad Request, dealer ID not provided"})

def get_dealer_details(request, dealer_id):
    if dealer_id:
        # Construct the endpoint for fetching dealer details using dealer_id
        endpoint = f"/fetchDealer/{dealer_id}"
        # Use the get_request function from restapis.py to get the dealer details
        dealership = get_request(endpoint)
        return JsonResponse({"status": 200, "dealer": dealership})
    else:
        return JsonResponse({"status": 400, "message": "Bad request, dealer ID not provided"})

@csrf_exempt
def add_review(request):
    # Check if the user is authenticated
    if not request.user.is_anonymous:
        try:
            # Parse the JSON request body
            data = json.loads(request.body)
            
            # Call the post_review method to submit the review data
            response = post_review(data)
            
            # Return the response as a JSON response
            return JsonResponse({"status": 200, "message": "Review posted successfully", "response": response})
        
        except json.JSONDecodeError:
            # Handle JSON parsing errors
            return JsonResponse({"status": 400, "message": "Invalid JSON format"}, status=400)
        
        except Exception as e:
            # Log the error and return an error message
            print(f"Error in posting review: {e}")
            return JsonResponse({"status": 500, "message": "Error in posting review"}, status=500)
    
    else:
        # If the user is not authenticated
        return JsonResponse({"status": 403, "message": "Unauthorized access"}, status=403)
