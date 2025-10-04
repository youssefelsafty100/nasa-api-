from django.db import models
import os
from django.conf import settings

# Create your models here.

class DZIImage(models.Model):
    title = models.CharField(max_length=255)
    dzi_file = models.CharField(max_length=500)  # Path to the .dzi file
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    @property
    def url(self):
        """Return the media URL for the DZI file"""
        return f"/media/{self.dzi_file}"
    
    class Meta:
        ordering = ['title']
