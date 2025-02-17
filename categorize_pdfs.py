import os

# Category aliases configuration
category_aliases = {
    'Soal': ['soal', 'coretan tutor', 'coret tutor', 'coretan', 'coret'],
    'Materi': ['materi'],
    'Kunci Jawaban': ['kunci jawaban', 'jawaban', 'pembahasan', 'coretan jawaban'],
    'Lain Lain': []
}

def get_category_from_filename(filename):
    """Automatically detect category from filename using configured aliases"""
    filename_lower = filename.lower()
    
    for category, aliases in category_aliases.items():
        if any(alias in filename_lower for alias in aliases):
            return category
    return 'Lain Lain'

def categorize_pdf(file_path):
    """Categorize a single PDF file"""
    # Get directory and filename
    directory = os.path.dirname(file_path)
    filename = os.path.basename(file_path)
    
    # Skip if file is already categorized
    categories = ['Soal_', 'Materi_', 'Kunci Jawaban_', 'Lain Lain_']
    if any(filename.startswith(category) for category in categories):
        print(f"Skipping already categorized file: {filename}")
        return
    
    # Get category from filename
    category = get_category_from_filename(filename)
    print(f"Auto-categorizing '{filename}' as: {category}")
    
    # Create new filename with category prefix
    new_filename = f"{category}_{filename}"
    new_file_path = os.path.join(directory, new_filename)
    
    try:
        # Rename the file
        os.rename(file_path, new_file_path)
        print(f"Successfully categorized as: {new_filename}")
    except Exception as e:
        print(f"Error categorizing {filename}: {str(e)}")

def main():
    departments_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'departments')
    
    if not os.path.exists(departments_dir):
        print(f"Error: {departments_dir} directory not found")
        return
    
    # Walk through all directories and files
    for root, dirs, files in os.walk(departments_dir):
        for filename in files:
            if filename.lower().endswith('.pdf'):
                file_path = os.path.join(root, filename)
                categorize_pdf(file_path)

if __name__ == '__main__':
    print("PDF Categorizer")
    print("This script will automatically categorize PDF files in the departments folder.")
    print("Press Ctrl+C at any time to exit.")
    try:
        main()
        print("\nCategorization complete!")
    except KeyboardInterrupt:
        print("\nCategorization interrupted by user.")