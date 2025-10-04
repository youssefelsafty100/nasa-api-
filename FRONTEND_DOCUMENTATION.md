# Frontend Developer API Documentation

## Base URL
```
http://127.0.0.1:8000
```

## Endpoint 1: Get Image List

**URL:** `GET /api/images/` (Note the trailing slash)

**Description:** Returns a JSON array of all processed DZI images.

**Full URL:** `http://127.0.0.1:8000/api/images/`

### Example Response:

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
    },
    {
        "id": 3,
        "title": "NGC 3372a-full",
        "url": "/media/NGC_3372a-full.dzi",
        "created_at": "2025-10-03T19:14:43.213789Z"
    },
    {
        "id": 4,
        "title": "Orion Nebula - Hubble 2006 mosaic 18000",
        "url": "/media/Orion_Nebula_-_Hubble_2006_mosaic_18000.dzi",
        "created_at": "2025-10-03T19:14:43.214123Z"
    },
    {
        "id": 5,
        "title": "The Orion Bar region (Hubble image) (weic2315d)",
        "url": "/media/The_Orion_Bar_region_(Hubble_image)_(weic2315d).dzi",
        "created_at": "2025-10-03T19:14:43.214456Z"
    },
    {
        "id": 6,
        "title": "Veil Nebula - NGC6960",
        "url": "/media/Veil_Nebula_-_NGC6960.dzi",
        "created_at": "2025-10-03T19:14:43.214789Z"
    },
    {
        "id": 7,
        "title": "opo0328a",
        "url": "/media/opo0328a.dzi",
        "created_at": "2025-10-03T19:14:43.215123Z"
    }
]
```

### Response Fields:

- **id**: Unique identifier for the image
- **title**: Human-readable title of the image
- **url**: Path to the DZI file (relative to base URL)
- **created_at**: Timestamp when the image was added to the database

## How to Use This API

### JavaScript Example:

```javascript
const baseUrl = "http://127.0.0.1:8000";

// Fetch the image list
fetch(`${baseUrl}/api/images/`)
  .then(response => response.json())
  .then(images => {
    console.log('Available images:', images);
    
    // Use the first image with OpenSeadragon
    if (images.length > 0) {
      const imageUrl = `${baseUrl}${images[0].url}`;
      
      OpenSeadragon({
        id: "viewer",
        tileSources: imageUrl
      });
    }
  })
  .catch(error => {
    console.error('Error fetching images:', error);
  });
```

### Complete OpenSeadragon Integration:

```javascript
const baseUrl = "http://127.0.0.1:8000";

async function loadImageViewer() {
  try {
    // Fetch image list from API
    const response = await fetch(`${baseUrl}/api/images/`);
    const images = await response.json();
    
    // Initialize OpenSeadragon viewer
    const viewer = OpenSeadragon({
      id: "viewer",
      prefixUrl: "https://cdn.jsdelivr.net/npm/openseadragon@4.1.0/build/openseadragon/images/",
      showNavigator: true,
      navigatorPosition: "TOP_RIGHT",
      showZoomControl: true,
      showHomeControl: true,
      showFullPageControl: true
    });
    
    // Function to load a specific image
    function loadImage(imageIndex) {
      const image = images[imageIndex];
      const dziUrl = `${baseUrl}${image.url}`;
      viewer.open(dziUrl);
    }
    
    // Load first image by default
    if (images.length > 0) {
      loadImage(0);
    }
    
    return { viewer, images, loadImage };
    
  } catch (error) {
    console.error('Failed to load images:', error);
  }
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', loadImageViewer);
```

### React Example:

```jsx
import React, { useState, useEffect } from 'react';
import OpenSeadragon from 'openseadragon';

const ImageViewer = () => {
  const [images, setImages] = useState([]);
  const [currentImage, setCurrentImage] = useState(0);
  const [viewer, setViewer] = useState(null);
  
  const baseUrl = "http://127.0.0.1:8000";

  useEffect(() => {
    // Fetch images from API
    fetch(`${baseUrl}/api/images/`)
      .then(response => response.json())
      .then(data => {
        setImages(data);
        initViewer(data);
      })
      .catch(error => console.error('Error:', error));
  }, []);

  const initViewer = (imageData) => {
    const osdViewer = OpenSeadragon({
      id: "openseadragon-viewer",
      prefixUrl: "https://cdn.jsdelivr.net/npm/openseadragon@4.1.0/build/openseadragon/images/",
      showNavigator: true,
      tileSources: imageData.length > 0 ? `${baseUrl}${imageData[0].url}` : null
    });
    setViewer(osdViewer);
  };

  const loadImage = (index) => {
    if (viewer && images[index]) {
      const imageUrl = `${baseUrl}${images[index].url}`;
      viewer.open(imageUrl);
      setCurrentImage(index);
    }
  };

  return (
    <div>
      <div className="image-selector">
        {images.map((image, index) => (
          <button 
            key={image.id}
            onClick={() => loadImage(index)}
            className={index === currentImage ? 'active' : ''}
          >
            {image.title}
          </button>
        ))}
      </div>
      <div id="openseadragon-viewer" style={{ width: '100%', height: '600px' }}></div>
    </div>
  );
};

export default ImageViewer;
```

## Important Notes:

1. **Base URL**: Replace `127.0.0.1:8000` with your actual server IP and port
2. **CORS**: The API allows cross-origin requests for development
3. **URL Construction**: Always concatenate `baseUrl + image.url` to get the full DZI path
4. **File Format**: All URLs point to `.dzi` files which contain Deep Zoom Image metadata
5. **Dependencies**: The API serves both the `.dzi` files and their associated tile directories automatically

## Testing the API:

You can test the API endpoint directly in your browser or with curl:

**Browser:** `http://127.0.0.1:8000/api/images/`

**curl:** 
```bash
curl http://127.0.0.1:8000/api/images/
```

## Error Handling:

The API returns standard HTTP status codes:
- **200**: Success
- **404**: Endpoint not found
- **500**: Server error

Always include error handling in your frontend code to gracefully handle network issues or API unavailability.