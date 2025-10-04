import os
from PIL import Image

# Make sure Pillow is up to date for best resampling quality
# pip install --upgrade Pillow

def create_deepzoom_pyramid(input_image_path, output_folder):
    """
    Creates a Deep Zoom Image (DZI) pyramid from a source image.
    """
    Image.MAX_IMAGE_PIXELS = None # Allow large images
    
    try:
        img = Image.open(input_image_path)
    except FileNotFoundError:
        print(f"Error: Could not find {input_image_path}")
        return
    except Exception as e:
        print(f"Error opening {input_image_path}: {e}")
        return

    # Create the files subfolder based on the image name
    image_name = os.path.splitext(os.path.basename(input_image_path))[0]
    files_folder = os.path.join(output_folder, f"{image_name}_files")
    if not os.path.exists(files_folder):
        os.makedirs(files_folder)

    width, height = img.size
    tile_size = 256
    
    # Calculate the number of zoom levels
    max_dim = max(width, height)
    level = 0
    temp_dim = max_dim
    while temp_dim > 1:
        temp_dim /= 2
        level += 1
    max_level = level

    # Loop through levels and create tiles
    for level in range(max_level, -1, -1):
        level_width = int(width / (2**(max_level - level)))
        level_height = int(height / (2**(max_level - level)))

        if level_width == 0 or level_height == 0:
            continue

        # Resize image for the current level
        resized_img = img.resize((level_width, level_height), Image.Resampling.LANCZOS)
        
        level_dir = os.path.join(files_folder, str(level))
        if not os.path.exists(level_dir):
            os.makedirs(level_dir)

        # Tile the resized image
        for y in range(0, level_height, tile_size):
            for x in range(0, level_width, tile_size):
                col = x // tile_size
                row = y // tile_size
                box = (x, y, x + tile_size, y + tile_size)
                tile = resized_img.crop(box)
                tile_path = os.path.join(level_dir, f"{col}_{row}.jpeg")
                tile.save(tile_path, "JPEG")

        print(f"Generated tiles for zoom level {level}")

    # Create the .dzi file (XML descriptor)
    dzi_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<Image TileSize="{tile_size}" Overlap="0" Format="jpeg" 
       xmlns="http://schemas.microsoft.com/deepzoom/2008">
    <Size Width="{width}" Height="{height}"/>
</Image>'''
    
    dzi_filename = f"{image_name}.dzi"
    dzi_path = os.path.join(output_folder, dzi_filename)
    with open(dzi_path, "w") as f:
        f.write(dzi_content)

    print(f"\nDeep Zoom pyramid for {os.path.basename(input_image_path)} created successfully! ✨")
    print(f"DZI file saved to: {dzi_path}")


if __name__ == "__main__":
    # 1. DEFINE FOLDERS
    source_folder = "images"               # <--- Folder containing your large images
    main_output_dir = "deepzoom_output"      # <--- Folder for all DZI outputs

    # 2. CHECK IF SOURCE FOLDER EXISTS
    if not os.path.isdir(source_folder):
        print(f"Error: Source folder '{source_folder}' not found.")
        print("Please create a folder named 'images' and put your images inside it.")
    else:
        # Create the main output directory if it doesn't exist
        if not os.path.exists(main_output_dir):
            os.makedirs(main_output_dir)

        # 3. DEFINE SUPPORTED IMAGE TYPES
        supported_extensions = ('.jpg', '.jpeg', '.png', '.tif', '.tiff', '.bmp')

        # 4. LOOP THROUGH IMAGES AND PROCESS THEM
        print(f"Starting to process images from '{source_folder}'...")
        for filename in os.listdir(source_folder):
            if filename.lower().endswith(supported_extensions):
                print(f"\n{'='*20}\nProcessing: {filename}\n{'='*20}")
                
                source_image_path = os.path.join(source_folder, filename)
                
                # Call the function for the current image
                create_deepzoom_pyramid(source_image_path, main_output_dir)
            else:
                print(f"\nSkipping non-image file: {filename}")
        
        print("\nAll images have been processed. ✅")