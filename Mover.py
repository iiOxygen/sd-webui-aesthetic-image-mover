import os
from os.path import join, isdir
from PIL import Image
import shutil
import configparser

def process_files(root_folder, output_folder):
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Iterate through each file in the root folder
    for filename in os.listdir(root_folder):
        # Skip files with specific names
        if filename in ['aesthetic', 'not_aesthetic']:
            continue
        
        # Get the full file path
        file_path = join(root_folder, filename)
        
        try:
            # Open the image file
            with Image.open(file_path) as img:
                # Get the PNG info
                png_info = img.info
                
                # Get the aesthetic score from the PNG info
                aesthetic_score = float(png_info.get("aesthetic_score", 0.0))
                
                # Determine the target folder based on the aesthetic score
                if aesthetic_score >= 7.0:
                    score_folder = "aesthetic"
                else:
                    score_folder = "not_aesthetic"
                
                # Create a decimal folder name based on the aesthetic score
                decimal_folder = "{:.1f}".format(aesthetic_score)
                
                # Create the target folder if it doesn't exist
                target_folder = os.path.join(output_folder, score_folder, decimal_folder)
                os.makedirs(target_folder, exist_ok=True)
                
                # Move the file to the target folder
                shutil.move(file_path, os.path.join(target_folder, filename))
        
        except PermissionError as e:
            # Print an error message if there is a permission error
            print(f"Error processing file {file_path}: {e}")

# Read the config.ini file
config = configparser.ConfigParser()
config.read('config.ini')

# Get the root_folder and output_folder from the config.ini file
root_folder = config.get('Paths', 'root_folder')
output_folder = config.get('Paths', 'output_folder')

# Process the root_folder
process_files(root_folder, output_folder)