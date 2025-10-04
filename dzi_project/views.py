from django.http import JsonResponse
from django.urls import path, include
from django.shortcuts import redirect, render
import os

def home_view(request):
    """
    Provides a simple JSON response for the home page.
    """
    api_info = {
        "message": "Welcome to the NASA Deep Zoom Image API",
        "description": "This server provides DZI data for space imagery.",
        "api_endpoint": "/api/",
        "usage": "Visit the API endpoint to get a JSON list of all available images."
    }
    return JsonResponse(api_info)

def redirect_to_api(request):
    """
    Redirect root URL to the images API endpoint
    """
    return redirect('/api/images/')