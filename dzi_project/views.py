import os
import json
from django.conf import settings
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# The view name can be anything, but the logic inside is what matters.
class DZIImageListView(APIView):
    def get(self, request, format=None):
        # Assumes data.json is in the root directory of your project
        json_file_path = os.path.join(settings.BASE_DIR, 'data.json')
        
        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return Response(data, status=status.HTTP_200_OK)
        except FileNotFoundError:
            return Response({"error": "data.json not found"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def home_view(request):
    """Render the home page with API documentation"""
    return render(request, 'home.html')