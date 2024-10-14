#!/usr/bin/env python3

import os
import shutil
import argparse
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Define file type categories
FILE_TYPES = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg'],
    'Documents': ['.txt', '.pdf', '.docx', '.doc', '.xlsx', '.xls', '.pptx', '.ppt', '.odt'],
    'Videos': ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv'],
    'Music': ['.mp3', '.wav', '.aac', '.flac', '.ogg'],
    'Archives': ['.zip', '.rar', '.tar', '.gz', '.bz2', '.7z'],
    'Scripts': ['.py', '.js', '.html', '.css', '.php', '.sh', '.bat'],
    # Add more categories as needed
}

def organize_files(source_dir):
    """
    Organizes files in the given directory into subdirectories based on file type.
    """
    # Iterate over all items in the directory
    for item in os.listdir(source_dir):
        item_path = os.path.join(source_dir, item)
        
        # Skip directories
        if os.path.isdir(item_path):
            logging.debug(f'Skipped directory: {item}')
            continue
        
        # Get the file extension
        _, file_ext = os.path.splitext(item)
        file_ext = file_ext.lower()
        
        # Determine the destination folder
        moved = False
        for category, extensions in FILE_TYPES.items():
            if file_ext in extensions:
                dest_dir = os.path.join(source_dir, category)
                os.makedirs(dest_dir, exist_ok=True)
                
                # Handle duplicate file names
                dest_path = os.path.join(dest_dir, item)
                dest_path = handle_duplicates(dest_path)
                
                shutil.move(item_path, dest_path)
                logging.info(f'Moved: {item} to {category}/')
                moved = True
                break
        
        # If the file extension doesn't match any category
        if not moved:
            dest_dir = os.path.join(source_dir, 'Others')
            os.makedirs(dest_dir, exist_ok=True)
            
            dest_path = os.path.join(dest_dir, item)
            dest_path = handle_duplicates(dest_path)
            
            shutil.move(item_path, dest_path)
            logging.info(f'Moved: {item} to Others/')

def handle_duplicates(dest_path):
    """
    Appends a number to the file name if a file with the same name already exists
    to avoid overwriting.
    """
    if not os.path.exists(dest_path):
        return dest_path
    else:
        base, extension = os.path.splitext(dest_path)
        i = 1
        new_dest_path = f"{base}({i}){extension}"
        while os.path.exists(new_dest_path):
            i += 1
            new_dest_path = f"{base}({i}){extension}"
        return new_dest_path

def parse_arguments():
    """
    Parses command-line arguments provided by the user.
    """
    parser = argparse.ArgumentParser(description='Organize files in a directory.')
    parser.add_argument('source', help='Source directory to organize')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    source_directory = args.source

    if os.path.isdir(source_directory):
        organize_files(source_directory)
        logging.info('File organization complete.')
    else:
        logging.error(f'The directory {source_directory} does not exist.')