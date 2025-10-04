# Django DZI API - Current Status

## API Information

**Base URL:** `http://127.0.0.1:8000`

**Available Endpoints:**
1. `GET /api/images/` - Returns JSON list of all DZI images
2. `GET /api/populate/` - Populates database from data.json (utility endpoint)

## API Response Format

### GET /api/images/

Returns a JSON array with the following structure for each image:

```json
{
  "id": 1,
  "title": "Image Title",
  "url": "/media/image_filename.dzi",
  "created_at": "2025-10-03T19:14:43.211234Z"
}
```

## Current Images in Database

1. Carina Nebula by ESO
2. Hubble M31Mosaic 2025
3. NGC 3372a-full
4. Orion Nebula - Hubble 2006 mosaic 18000
5. The Orion Bar region (Hubble image) (weic2315d)
6. Veil Nebula - NGC6960
7. opo0328a

## How to Use the API

### For Frontend Developers:

```javascript
// Base URL
const baseUrl = "http://127.0.0.1:8000";

// Fetch all images
fetch(`${baseUrl}/api/images/`)
  .then(response => response.json())
  .then(images => {
    // Use the first image with OpenSeadragon
    const firstImage = images[0];
    const dziUrl = `${baseUrl}${firstImage.url}`;
    
    // Initialize OpenSeadragon viewer
    OpenSeadragon({
      id: "viewer",
      tileSources: dziUrl
    });
  });
```

## File Structure

```
media/
├── Carina_Nebula_by_ESO.dzi
├── Carina_Nebula_by_ESO_files/
├── Hubble_M31Mosaic_2025.dzi
├── Hubble_M31Mosaic_2025_files/
├── NGC_3372a-full.dzi
├── NGC_3372a-full_files/
├── Orion_Nebula_-_Hubble_2006_mosaic_18000.dzi
├── Orion_Nebula_-_Hubble_2006_mosaic_18000_files/
├── The_Orion_Bar_region_(Hubble_image)_(weic2315d).dzi
├── The_Orion_Bar_region_(Hubble_image)_(weic2315d)_files/
├── Veil_Nebula_-_NGC6960.dzi
├── Veil_Nebula_-_NGC6960_files/
├── opo0328a.dzi
└── opo0328a_files/
```

## Server Status

✅ Django development server running on port 8000
✅ Database populated with 7 images
✅ Media files properly served from /media/ endpoint
✅ API endpoints functional
✅ CORS enabled for frontend integration

## Testing URLs

1. API endpoint: http://127.0.0.1:8000/api/images/
2. Sample DZI file: http://127.0.0.1:8000/media/Carina_Nebula_by_ESO.dzi
3. Admin panel (if needed): http://127.0.0.1:8000/admin/

## Notes

- The server is configured for development use only
- All DZI files and their associated tile directories are properly served
- The database is SQLite and already populated
- No authentication is required for API access