import os
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from pathlib import Path

def get_file_creation_time(filepath):
    """Get file modification time and return in EXIF format"""
    mtime = os.path.getmtime(filepath)
    dt = datetime.fromtimestamp(mtime)
    return dt.strftime("%Y:%m:%d %H:%M:%S")

def process_image(filepath):
    """Process a single image file"""
    print(f"Processing {filepath}")
    try:
        # Open image and get EXIF data
        with Image.open(filepath) as img:
            exif = img.getexif()
            
            # Check if image has EXIF data
            if not exif:
                exif = {}
            
            # Look for DateTimeOriginal (tag 36867)
            if 36867 not in exif:
                # Get file creation time
                creation_time = get_file_creation_time(filepath)
                
                # Create new EXIF data
                img.info['exif'] = exif
                exif[36867] = creation_time
                
                # Save image with new EXIF data
                img.save(filepath, exif=exif)
                print(f"Updated creation time for {filepath}")
            
    except Exception as e:
        print(f"Error processing {filepath}: {str(e)}")

def main():
    # Get current directory
    current_dir = Path("/Users/ph/Desktop/wcef/")
    
    # Process all image files
    for filepath in current_dir.glob("*"):
        print(filepath)
        if filepath.suffix.lower() in ['.jpg', '.jpeg', '.tiff', '.png']:
            process_image(str(filepath))

if __name__ == "__main__":
    main()
