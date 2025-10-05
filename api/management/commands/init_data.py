import os
import json
from django.core.management.base import BaseCommand
from django.conf import settings
from api.models import DZIImage

class Command(BaseCommand):
    help = 'Initialize database with data from data.json'

    def handle(self, *args, **options):
        # Read the data.json file
        data_json_path = os.path.join(settings.BASE_DIR, 'data.json')
        
        if not os.path.exists(data_json_path):
            self.stdout.write(
                self.style.ERROR('data.json file not found')
            )
            return
        
        try:
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
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully populated database with {created_count} new images. '
                    f'Total images: {DZIImage.objects.count()}'
                )
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error initializing data: {str(e)}')
            )