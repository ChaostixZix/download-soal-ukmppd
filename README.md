# Medical PDF Organizer

This Python script helps organize medical PDF files into department-specific folders based on their filenames. It supports both English and Indonesian department names.

## Installation

1. Make sure you have Python 3.6 or higher installed
2. Install the required dependencies using pip:

```bash
pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

## Setup

1. Create a folder named `study-materials` in the same directory as the script
2. Place all your PDF files in the `study-materials` folder

## Usage

Run the script using Python:

```bash
python organize_pdfs.py
```

The script will:
1. Create folders for each medical department
2. Scan all PDFs in the `study-materials` folder
3. Move each PDF to its corresponding department folder based on the filename
4. Place files without a clear department reference in the "Lain-lain" folder

## Supported Departments

- Obstetrics and Gynecology (OBGYN)
- Surgery
- Internal Medicine
- Pediatrics
- Neurology
- Cardiology
- Dermatology
- Ophthalmology
- ENT
- Psychiatry
- Radiology
- Anesthesiology
- Orthopedics
- Urology
- Pulmonology

Files that don't match any department keywords will be moved to the "Lain-lain" folder.

## Note

The script looks for department keywords in both English and Indonesian in the filenames. For example:
- "Obgsyn-soal1.pdf" → Obstetrics and Gynecology folder
- "soal-bedah.pdf" → Surgery folder