import pdfplumber
from tqdm.notebook import tqdm
import re
import pickle
import pytesseract
from pdf2image import convert_from_path


def extract_text_from_pdf_atlas(pdf_atlas_path):
    with pdfplumber.open(pdf_atlas_path) as pdf:
        texts = ''
        for page in tqdm(pdf.pages):
            line_x = page.width / 2 - 25
            left_column_text = ''
            right_colum_text = ''
            for obj in page.extract_words():
                if obj['x0'] < line_x:
                    left_column_text += obj['text'] + ' '
                else:
                    right_colum_text += obj['text'] + ' '
            texts += left_column_text + right_colum_text
    pdf.close()
    return texts


def extract_images_from_pdf(pdf_path):
    images = convert_from_path(pdf_path)
    return images


def read_text_from_image(image):
    text = pytesseract.image_to_string(image, lang='rus+eng')
    return text


def extract_text_from_pdf_ussr(ussr_pdf_path):
    images = extract_images_from_pdf(ussr_pdf_path)
    texts = ''
    for image in tqdm(images):
        text = read_text_from_image(image)
        texts += text
    return texts


def extract_text_from_pdf_drugs(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        texts = ''
        for page in tqdm(pdf.pages):
            text = page.extract_text()
            texts += text
    pdf.close()
    return text


def clean_extracted_text(extracted_text):
    cleaned_text = extracted_text.replace('\n', ' ')
    cleaned_text = cleaned_text.replace('  ', ' ')
    cleaned_text = cleaned_text.replace('}', ')')
    cleaned_text = cleaned_text.replace('{', '(')
    pattern = r'(\w)-\s'
    cleaned_text = re.sub(pattern, r'\1', cleaned_text)
    return cleaned_text


def save_with_pickle(text, file_name):
    with open(file_name, 'wb') as file:
        pickle.dump(text, file)
    with open(file_name, 'rb') as file:
        done = pickle.load(file)
    print(done[:10000])