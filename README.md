# Django DZI API

This Django REST API serves Deep Zoom Image (DZI) files for use with OpenSeadragon or other deep zoom viewers.

## Features

- REST API to list all available DZI images
- Automatic population of database from `data.json`
- Proper media file serving for DZI files and tiles
- CORS support for frontend integration
- Easy integration with OpenSeadragon

## Setup Instructions

### 1. Install Dependencies

```bash
pip install django djangorestframework
```

### 2. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Populate Database

First, make sure your `deepzoom_output` folder is copied to the `media` directory (this should already be done).

Then populate the database from your existing `data.json`:

```bash
curl http://127.0.0.1:8000/api/populate/
```

### 4. Start Development Server

```bash
python manage.py runserver
```

Your API will be available at: `http://127.0.0.1:8000`

## API Endpoints

### GET /api/images/

Returns a JSON array of all processed DZI images.

**Example Response:**
```json
[
    {
        "id": 1,
        "title": "Carina Nebula by ESO",
        "url": "/media/Carina_Nebula_by_ESO.dzi",
        "created_at": "2025-10-03T19:14:43.211234Z"
    },
    {
        "id": 2,
        "title": "Hubble M31Mosaic 2025",
        "url": "/media/Hubble_M31Mosaic_2025.dzi",
        "created_at": "2025-10-03T19:14:43.213456Z"
    }
]
```

### GET /api/populate/

Populates the database from the existing `data.json` file. This is a utility endpoint.

**Example Response:**
```json
{
    "message": "Successfully populated database with 7 new images",
    "total_images": 7
}
```

## Frontend Integration

### JavaScript Example

```javascript
const baseUrl = "http://127.0.0.1:8000";

// Fetch image list
async function fetchImages() {
    const response = await fetch(`${baseUrl}/api/images/`);
    const images = await response.json();
    return images;
}

// Use with OpenSeadragon
function loadImage(image) {
    const dziUrl = `${baseUrl}${image.url}`;
    
    OpenSeadragon({
        id: "viewer",
        tileSources: dziUrl
    });
}
```

### Full HTML Example

See `api_test.html` for a complete working example with OpenSeadragon integration.

## File Structure

```
d:/courses/Nasa/
├── manage.py                    # Django management script
├── dzi_project/                 # Django project settings
│   ├── settings.py             # Django configuration
│   ├── urls.py                 # Main URL configuration
│   └── ...
├── api/                        # Django API app
│   ├── models.py               # DZIImage model
│   ├── views.py                # API views
│   ├── serializers.py          # DRF serializers
│   ├── urls.py                 # API URL patterns
│   └── ...
├── media/                      # Media files (DZI + tiles)
│   ├── Carina_Nebula_by_ESO.dzi
│   ├── Carina_Nebula_by_ESO_files/
│   ├── Hubble_M31Mosaic_2025.dzi
│   ├── Hubble_M31Mosaic_2025_files/
│   └── ...
├── data.json                   # Original image metadata
├── api_test.html               # Test page for the API
└── README.md                   # This file
```

## Production Deployment

For production deployment:

1. Set `DEBUG = False` in `settings.py`
2. Configure `ALLOWED_HOSTS` with your domain
3. Use a production WSGI server (gunicorn, uwsgi)
4. Serve static/media files with nginx or similar
5. Use environment variables for sensitive settings

### Environment Variables Example

```python
import os
from pathlib import Path

# settings.py
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost').split(',')
```

## Notes

- The API uses Django REST Framework for consistent JSON responses
- Media files are served directly by Django in development
- All DZI files and their tile directories must be in the `media/` folder
- The database automatically tracks all available images
- CORS is enabled for cross-origin requests

## Troubleshooting

### Images not loading
- Verify DZI files are in the `media/` directory
- Check that the Django server is running
- Ensure the `populate` endpoint was called to load image metadata

### CORS issues
- The API allows all origins in development
- For production, configure CORS properly in `settings.py`

### File serving issues
- In development, Django serves media files automatically
- In production, configure your web server to serve the `/media/` path