import os
import json

def create_image_list(dzi_folder="deepzoom_output"):
    """
    Scans a folder for .dzi files and creates a JSON list for the webpage.
    """
    images = []
    
    if not os.path.isdir(dzi_folder):
        print(f"Error: Directory '{dzi_folder}' not found.")
        print("Please run the 'process_images.py' script first.")
        return

    # Find all .dzi files in the output directory
    for filename in sorted(os.listdir(dzi_folder)):
        if filename.lower().endswith(".dzi"):
            image_name = os.path.splitext(filename)[0]
            image_path = os.path.join(dzi_folder, filename)
            
            # Add image info to our list
            images.append({
                "title": image_name.replace("_", " "), # Make a nice title
                "url": image_path.replace("\\", "/") # Use forward slashes for web paths
            })

    # Write the list to a data.json file
    with open("data.json", "w") as f:
        json.dump(images, f, indent=4)

    print(f"✅ Successfully created data.json with {len(images)} images.")

if __name__ == "__main__":
    create_image_list()