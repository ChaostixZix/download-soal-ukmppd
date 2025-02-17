import os

# Dictionary mapping department keywords (both English and Indonesian)
department_keywords = {
    'Obstetrics and Gynecology': ['obgyn', 'obsgin', 'kandungan', 'kebidanan'],
    'Surgery': ['bedah', 'surgery', 'surgical'],
    'Internal Medicine': ['interna', 'internal', 'penyakit dalam'],
    'Pediatrics': ['anak', 'pediatric', 'pediatri'],
    'Neurology': ['saraf', 'neuro', 'neurologi'],
    'Cardiology': ['jantung', 'cardio', 'kardiologi'],
    'Dermatology': ['kulit', 'derma', 'dermatologi'],
    'Ophthalmology': ['mata', 'eye', 'ophthal'],
    'ENT': ['tht', 'ent', 'telinga'],
    'Psychiatry': ['jiwa', 'psikiatri', 'psychiatric'],
    'Radiology': ['radiologi', 'radiology', 'rontgen'],
    'Anesthesiology': ['anestesi', 'anesthesia'],
    'Orthopedics': ['ortho', 'ortopedi', 'tulang'],
    'Urology': ['urologi', 'urology'],
    'Pulmonology': ['paru', 'pulmo', 'respirologi'],
    'Nephrology': ['ginjal', 'nefro', 'nephro', 'renal']
}

def count_pdfs_in_departments():
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Dictionary to store counts
    pdf_counts = {}
    
    # Count PDFs in each department folder
    for department in department_keywords.keys():
        department_path = os.path.join(current_dir, department)
        if os.path.exists(department_path):
            pdf_files = [f for f in os.listdir(department_path) if f.lower().endswith('.pdf')]
            pdf_counts[department] = len(pdf_files)
        else:
            pdf_counts[department] = 0
    
    # Count PDFs in 'Lain-lain' folder
    lain_lain_path = os.path.join(current_dir, 'Lain-lain')
    if os.path.exists(lain_lain_path):
        pdf_files = [f for f in os.listdir(lain_lain_path) if f.lower().endswith('.pdf')]
        pdf_counts['Lain-lain'] = len(pdf_files)
    else:
        pdf_counts['Lain-lain'] = 0
    
    return pdf_counts

def main():
    pdf_counts = count_pdfs_in_departments()
    
    # Print results
    print("\nPDF Count by Department:")
    print("-" * 40)
    
    # Calculate total PDFs
    total_pdfs = sum(pdf_counts.values())
    
    # Print counts for each department
    for department, count in sorted(pdf_counts.items()):
        print(f"{department}: {count} PDFs")
    
    print("-" * 40)
    print(f"Total PDFs: {total_pdfs}")

if __name__ == '__main__':
    main()