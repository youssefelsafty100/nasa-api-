from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.conf import settings
import os
import json
from .models import DZIImage
from .serializers import DZIImageSerializer

# Create your views here.

class DZIImageListView(generics.ListAPIView):
    """API endpoint to list all DZI images"""
    queryset = DZIImage.objects.all()
    serializer_class = DZIImageSerializer


@api_view(['GET'])
def populate_from_data_json(request):
    """Populate database from the existing data.json file"""
    try:
        # Read the data.json file
        data_json_path = os.path.join(settings.BASE_DIR, 'data.json')
        
        if not os.path.exists(data_json_path):
            return Response({'error': 'data.json file not found'}, status=404)
        
        with open(data_json_path, 'r') as f:
            images_data = json.load(f)
        
        created_count = 0
        for image_data in images_data:
            # Extract filename from URL for the dzi_file field
            url = image_data['url']
            # Remove 'deepzoom_output/' prefix to get just the filename
            dzi_file = url.replace('deepzoom_output/', '')
            
            # Create or update the DZI image record
            obj, created = DZIImage.objects.get_or_create(
                title=image_data['title'],
                defaults={'dzi_file': dzi_file}
            )
            
            if created:
                created_count += 1
        
        return Response({
            'message': f'Successfully populated database with {created_count} new images',
            'total_images': DZIImage.objects.count()
        })
        
    except Exception as e:
        return Response({'error': str(e)}, status=500)