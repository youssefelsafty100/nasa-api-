import os
import json
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view


class ImageListView(APIView):
    def get(self, request, format=None):
        # Assumes data.json is in the project's root directory
        json_file_path = os.path.join(settings.BASE_DIR, 'data.json')
        
        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return Response(data, status=status.HTTP_200_OK)
        except FileNotFoundError:
            return Response({"error": "data.json not found"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def populate_from_data_json(request):
    """Utility function to confirm data.json is accessible"""
    try:
        # Read the data.json file
        data_json_path = os.path.join(settings.BASE_DIR, 'data.json')
        
        if not os.path.exists(data_json_path):
            return Response({'error': 'data.json file not found'}, status=status.HTTP_404_NOT_FOUND)
        
        with open(data_json_path, 'r') as f:
            images_data = json.load(f)
        
        return Response({
            'message': 'Data.json file is accessible',
            'total_images': len(images_data)
        })
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)