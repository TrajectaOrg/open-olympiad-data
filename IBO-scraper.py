import os
import PyPDF2
import pandas as pd
import logging
from concurrent.futures import ThreadPoolExecutor

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def process_pdf(pdf_path, excel_path):
    try:
        with open(pdf_path, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            text_data = []

            for page in reader.pages:
                text = page.extract_text()
                if text:
                    text_data.append(text.strip())  # Clean text

            if text_data:
                df = pd.DataFrame(text_data, columns=['Text'])
                df.to_excel(excel_path, index=False)  # Save to Excel
                logging.info(f'Successfully processed {pdf_path}')
            else:
                logging.warning(f'No text found in {pdf_path}')

    except Exception as e:
        logging.error(f'Error processing {pdf_path}: {e}')

def pdf_to_excel(pdf_folder, excel_folder):
    os.makedirs(excel_folder, exist_ok=True)

    pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith('.pdf')]
    with ThreadPoolExecutor() as executor:
        for filename in pdf_files:
            pdf_path = os.path.join(pdf_folder, filename)
            excel_path = os.path.join(excel_folder, filename.replace('.pdf', '.xlsx'))  # Change extension to .xlsx
            executor.submit(process_pdf, pdf_path, excel_path)

# Example usage
pdf_to_excel('IBO/', 'Excel/')
