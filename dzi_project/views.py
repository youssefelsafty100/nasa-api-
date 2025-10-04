from django.http import JsonResponse
from django.urls import path, include
from django.shortcuts import redirect, render
import os

def home_view(request):
    """
    Home page view that provides API information
    """
    # Check if template exists
    template_path = os.path.join(os.path.dirname(__file__), '..', 'templates', 'home.html')
    if os.path.exists(template_path):
        return render(request, 'home.html')
    else:
        # Fallback to JSON response if template doesn't exist
        api_info = {
            "message": "Django DZI API Server",
            "description": "This server provides Deep Zoom Image (DZI) files for use with OpenSeadragon or other viewers.",
            "endpoints": {
                "images_list": "/api/images/",
                "populate_database": "/api/populate/"
            },
            "usage": "Visit /api/images/ to get a JSON list of all available DZI images",
            "documentation": "See FRONTEND_DOCUMENTATION.md for integration instructions"
        }
        return JsonResponse(api_info)

def redirect_to_api(request):
    """
    Redirect root URL to the images API endpoint
    """
    return redirect('/api/images/')