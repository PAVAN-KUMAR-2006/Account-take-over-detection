import os
import zipfile

def create_zip():
    zip_filename = '../AI26CY01_Final_Project.zip'
    exclude_dirs = {'node_modules', 'venv', '__pycache__', '.git', '.vite'}
    exclude_exts = {'.pyc'}
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk('.'):
            # Modify dirs in-place to skip excluded directories
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            for file in files:
                if any(file.endswith(ext) for ext in exclude_exts):
                    continue
                file_path = os.path.join(root, file)
                zipf.write(file_path, arcname=file_path)
                
    print(f"Created {zip_filename}")

if __name__ == '__main__':
    create_zip()

