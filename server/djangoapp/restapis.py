# Uncomment the imports below before you add the function code
import requests
import os
from dotenv import load_dotenv

load_dotenv()

backend_url = os.getenv(
    'backend_url', default="https://panucciodonn-3030.theiadockernext-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/")
sentiment_analyzer_url = os.getenv(
    'sentiment_analyzer_url',
    default="http://localhost:5050/")

# Function for GET requests to backend
def get_request(endpoint, **kwargs):
    params = ""
    if(kwargs):
        for key, value in kwargs.items():
            params = params + key + "=" + value + "&"
    request_url = backend_url + endpoint + "?" + params
    print("GET from {} ".format(request_url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(request_url)
        return response.json()
    except Exception as e:
        # If any error occurs
        print(f"Network exception occurred: {e}")

# def analyze_review_sentiments(text):
# request_url = sentiment_analyzer_url+"analyze/"+text
# Add code for retrieving sentiments

def post_review(data_dict):
    # Construct the URL for posting the review
    request_url = backend_url + "/insert_review"
    print(f"POST to {request_url} with data: {data_dict}")

    try:
        # Send the POST request with the review data as JSON
        response = requests.post(request_url, json=data_dict)

        # Print and return the JSON response from the backend
        print(response.json())
        return response.json()
    except requests.exceptions.RequestException as e:
        # Handle any exceptions that occur during the request
        print(f"Network exception occurred: {e}")
        return {"error": "Network exception occurred"}
