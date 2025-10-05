# Django DZI API

This Django REST API serves Deep Zoom Image (DZI) files for use with OpenSeadragon or other deep zoom viewers.

## Features

- REST API to list all available DZI images
- Automatic population of database from `data.json`
- Proper media file serving for DZI files and tiles
- CORS support for frontend integration
- Easy integration with OpenSeadragon

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd nasa-api
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Variables

Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

Then edit the `.env` file to set your environment variables:

- `SECRET_KEY`: Django secret key (required for production)
- `DEBUG`: Set to `False` for production
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts

### 4. Obtain DZI Files

This repository does not include the actual DZI files due to their large size. You need to obtain them separately and place them in the `media/` directory.

If you have your own DZI files:
1. Place your `.dzi` files and their corresponding `_files` directories in the `media/` directory
2. Update the `data.json` file with the metadata for your images

If you want to use sample NASA images:
1. Download the deep zoom images from the source
2. Extract them to the `media/` directory
3. Ensure the structure matches what's expected in `data.json`

### 5. Run Migrations

```bash
python manage.py migrate
```

### 6. Populate Database

Populate the database from your existing `data.json`:

```bash
python manage.py init_data
```

Alternatively, you can use the API endpoint:
```bash
curl http://127.0.0.1:8000/api/populate/
```

### 7. Start Development Server

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
├── media/                      # Media files (DZI + tiles) - NOT included in repo
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

1. Set `DEBUG = False` in environment variables
2. Configure `ALLOWED_HOSTS` with your domain
3. Use a production WSGI server (gunicorn, uwsgi)
4. Serve static/media files with nginx or similar
5. Use a strong SECRET_KEY

### Environment Variables Example

```bash
# .env file
DEBUG=False
SECRET_KEY=your-very-secure-secret-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

### Vercel Deployment

The project is configured for Vercel deployment with the `vercel.json` file. During deployment:

1. The `build_files.sh` script runs to:
   - Unzip deep zoom assets (if deepzoom_output.zip exists)
   - Install dependencies
   - Run migrations
   - Initialize data
2. The database is configured to use `/tmp/db.sqlite3` which is writable on Vercel

## Security Notes

- Never commit your `.env` file to version control
- Always use a strong, random SECRET_KEY in production
- The default SECRET_KEY in the code is only for development
- Set DEBUG=False in production environments

## Troubleshooting

### Images not loading
- Verify DZI files are in the `media/` directory
- Check that the Django server is running
- Ensure the database was populated with image metadata

### CORS issues
- The API allows all origins in development
- For production, configure CORS properly in `settings.py`

### File serving issues
- In development, Django serves media files automatically
- In production, configure your web server to serve the `/media/` path