import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get URLs from environment variables
backend_url = os.getenv(
    'backend_url', default="https://panucciodonn-3030.theiadockernext-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/")
sentiment_analyzer_url = os.getenv(
    'sentiment_analyzer_url',
    default="http://localhost:5050/")

# Function for GET requests to backend
def get_request(endpoint, **kwargs):
    # Construct the query parameters string from kwargs
    params = "&".join([f"{key}={value}" for key, value in kwargs.items()])
    request_url = f"{backend_url}{endpoint}?{params}" if params else f"{backend_url}{endpoint}"
    print(f"GET from {request_url}")

    try:
        # Send the GET request
        response = requests.get(request_url)
        response.raise_for_status()  # Raise an exception for 4xx/5xx responses
        return response.json()
    except requests.exceptions.RequestException as e:
        # Handle network or request errors
        print(f"Network exception occurred: {e}")
        return {"error": "Network exception occurred"}

# Function for sentiment analysis
def analyze_review_sentiments(text):
    request_url = f"{sentiment_analyzer_url}analyze/"
    print(f"POST to {request_url} for sentiment analysis of text: {text}")

    try:
        # Send the POST request with text to analyze
        response = requests.post(request_url, json={"text": text})
        response.raise_for_status()  # Raise an exception for 4xx/5xx responses

        # Extract and return the sentiment from the response
        sentiment = response.json().get("sentiment", "neutral")
        return {"sentiment": sentiment}
    except requests.exceptions.RequestException as e:
        print(f"Network exception occurred during sentiment analysis: {e}")
        return {"sentiment": "neutral"}

# Function for POST requests to submit review data
def post_review(data_dict):
    request_url = f"{backend_url}/insert_review"
    print(f"POST to {request_url} with data: {data_dict}")

    try:
        # Send the POST request with the review data as JSON
        response = requests.post(request_url, json=data_dict)
        response.raise_for_status()  # Raise an exception for 4xx/5xx responses

        # Print and return the JSON response from the backend
        print(response.json())
        return response.json()
    except requests.exceptions.RequestException as e:
        # Handle any network or request errors
        print(f"Network exception occurred: {e}")
        return {"error": "Network exception occurred"}
