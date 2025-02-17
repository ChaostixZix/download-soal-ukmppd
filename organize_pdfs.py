import os
import shutil
import re

# Dictionary mapping department keywords (both English and Indonesian)
department_keywords = {
    'Obstetrics and Gynecology': ['obgyn', 'obsgin', 'kandungan', 'kebidanan', 'obsgyn'],
    'Surgery': ['bedah', 'surgery', 'surgical'],
    'Internal Medicine': ['interna', 'internal', 'penyakit dalam', 'geh', 'endokrin', 'endo', 'ipd'],
    'Pediatrics': ['anak', 'pediatric', 'pediatri'],
    'Neurology': ['saraf', 'neuro', 'neurologi'],
    'Cardiology': ['jantung', 'cardio', 'kardiologi'],
    'Dermatology': ['kulit', 'derma', 'dermatologi'],
    'Ophthalmology': ['mata', 'eye', 'ophthal', 'oftalmologi'],
    'ENT': ['tht', 'ent', 'telinga'],
    'Psychiatry': ['jiwa', 'psikiatri', 'psychiatric'],
    'Radiology': ['radiologi', 'radiology', 'rontgen'],
    'Anesthesiology': ['anestesi', 'anesthesia'],
    'Orthopedics': ['ortho', 'ortopedi', 'tulang'],
    'Urology': ['urologi', 'urology'],
    'Pulmonology': ['paru', 'pulmo', 'respirologi'],
    'Nephrology': ['ginjal', 'nefro', 'nephro', 'renal'],
    'Tropical Infection': ['tropis', 'tropical', 'infeksi', 'infection', 'parasit', 'parasite', 'malaria', 'dengue', 'dbd'],
    'Forensics': ['forensik', 'forensics', 'medikolegal', 'forensic', 'medicolegal', 'legal medicine', 'hukum kedokteran']
}

def create_department_folders(base_dir):
    """Create folders for each department and 'Lain-lain' inside departments folder"""
    # Create main departments directory
    departments_dir = os.path.join(base_dir, 'departments')
    os.makedirs(departments_dir, exist_ok=True)
    
    for department in department_keywords.keys():
        folder_path = os.path.join(departments_dir, department)
        os.makedirs(folder_path, exist_ok=True)
    
    # Create 'Lain-lain' folder for unclassified files
    os.makedirs(os.path.join(departments_dir, 'Lain-lain'), exist_ok=True)

def get_department(filename):
    """Determine department based on filename"""
    filename_lower = filename.lower()
    
    for department, keywords in department_keywords.items():
        for keyword in keywords:
            if keyword.lower() in filename_lower:
                return department
    
    return 'Lain-lain'

def process_pdf_file(source_path, base_dir):
    """Process a single PDF file"""
    filename = os.path.basename(source_path)
    department = get_department(filename)
    dest_folder = os.path.join(base_dir, 'departments', department)
    dest_path = os.path.join(dest_folder, filename)
    
    try:
        shutil.copy2(source_path, dest_path)
        print(f"Moved '{filename}' to departments/{department} folder")
        # Delete the source file after successful copy
        os.remove(source_path)
        print(f"Deleted original file: '{filename}'")
    except Exception as e:
        print(f"Error processing '{filename}': {str(e)}")

def organize_pdfs(source_dir, base_dir):
    """Recursively organize PDFs from source directory and its subfolders"""
    if not os.path.exists(source_dir):
        print(f"Error: Source directory '{source_dir}' does not exist")
        return
    
    # Create department folders
    create_department_folders(base_dir)
    
    # Walk through all directories and subdirectories
    for root, dirs, files in os.walk(source_dir):
        for filename in files:
            if filename.lower().endswith('.pdf'):
                source_path = os.path.join(root, filename)
                process_pdf_file(source_path, base_dir)

def main():
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define source and base directories
    source_dir = os.path.join(current_dir, 'downloads')
    base_dir = current_dir
    
    print("Starting PDF organization...")
    organize_pdfs(source_dir, base_dir)
    print("PDF organization completed!")

if __name__ == '__main__':
    main()