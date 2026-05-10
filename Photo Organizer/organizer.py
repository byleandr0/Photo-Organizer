import os
import shutil
from config import IMAGE_EXTENSIONS

def get_files(target_folder):
    """Reads the folder and returns a list of tuples: (filename, extension)"""
    files = []
    try:
        for filename in os.listdir(target_folder):
            filepath = os.path.join(target_folder, filename)
            if os.path.isfile(filepath):
                _, ext = os.path.splitext(filename)
                if ext.lower() in IMAGE_EXTENSIONS:
                    files.append((filename, ext.upper()))
        return files
    except Exception as e:
        raise Exception(f"Error reading folder: {e}")

def generate_preview(target_folder, project_name, client_prefix, original_files):
    """
    Simulates the organization process. Calculates the new name and checks for existing files.
    Returns a list of dictionaries with preview data.
    """
    preview = []
    counter = 1
    clean_prefix = client_prefix.rstrip('_')
    
    for filename, _ in original_files:
        _, ext = os.path.splitext(filename)
        ext = ext.lower()
        
        folder_ext_name = ext.replace(".", "").upper()
        dest_folder = os.path.join(target_folder, project_name, folder_ext_name)
        
        new_name = f"{clean_prefix}_{counter}{ext}"
        new_filepath = os.path.join(dest_folder, new_name)
        
        
        conflict = os.path.exists(new_filepath)
        
        preview.append({
            'original': filename,
            'new_name': new_name,
            'dest_folder': dest_folder,
            'new_filepath': new_filepath,
            'old_filepath': os.path.join(target_folder, filename),
            'conflict': conflict,
            'status': 'Ready to move' if not conflict else '⚠️ ALREADY EXISTS!'
        })
        counter += 1
    return preview

def execute_organization(preview_data):
    """Physically moves and renames the files."""
    successes = 0
    errors = 0
    
    for item in preview_data:
        try:
            os.makedirs(item['dest_folder'], exist_ok=True)
            shutil.move(item['old_filepath'], item['new_filepath'])
            item['status'] = '✅ Moved'
            successes += 1
        except Exception as e:
            item['status'] = f'❌ Error'
            errors += 1
            
    return successes, errors
