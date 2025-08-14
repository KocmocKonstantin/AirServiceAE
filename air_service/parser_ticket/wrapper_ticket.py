import fitz 
import cv2
import pytesseract
from PIL import Image
import numpy as np
import tempfile
import os

def extract_text_from_pdf(pdf_path):
    text = ""
    doc = fitz.open(pdf_path)
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

def extract_text_from_image(image_path):
    # Загружаем изображение
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Не удалось загрузить изображение: {image_path}")
    
    # Конвертируем в оттенки серого
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Список для хранения результатов разных методов обработки
    texts = []
    
    # Метод 1: Бинаризация
    _, thresh1 = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    text1 = pytesseract.image_to_string(thresh1, lang='rus+eng', config='--psm 6')
    texts.append(text1)
    
    # Метод 2: Адаптивная бинаризация
    thresh2 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    text2 = pytesseract.image_to_string(thresh2, lang='rus+eng', config='--psm 6')
    texts.append(text2)
    
    # Метод 3: Увеличение контрастности
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enhanced = clahe.apply(gray)
    _, thresh3 = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    text3 = pytesseract.image_to_string(thresh3, lang='rus+eng', config='--psm 6')
    texts.append(text3)
    
    # Метод 4: Удаление шума с помощью морфологических операций
    kernel = np.ones((1,1), np.uint8)
    denoised = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)
    _, thresh4 = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    text4 = pytesseract.image_to_string(thresh4, lang='rus+eng', config='--psm 6')
    texts.append(text4)
    
    # Метод 5: Масштабирование изображения для лучшего распознавания
    height, width = gray.shape
    scale_factor = 2
    scaled = cv2.resize(gray, (width * scale_factor, height * scale_factor), interpolation=cv2.INTER_CUBIC)
    _, thresh5 = cv2.threshold(scaled, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    text5 = pytesseract.image_to_string(thresh5, lang='rus+eng', config='--psm 6')
    texts.append(text5)
    
    # Метод 6: Поворот изображения для поиска лучшего угла
    angles = [-2, -1, 0, 1, 2]  # Небольшие повороты
    for angle in angles:
        if angle == 0:
            rotated = gray
        else:
            height, width = gray.shape
            center = (width // 2, height // 2)
            rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
            rotated = cv2.warpAffine(gray, rotation_matrix, (width, height))
        
        _, thresh_rot = cv2.threshold(rotated, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        text_rot = pytesseract.image_to_string(thresh_rot, lang='rus+eng', config='--psm 6')
        texts.append(text_rot)
    
    # Объединяем все результаты, удаляя дубликаты и пустые строки
    combined_text = ""
    seen_lines = set()
    
    for text in texts:
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if line and len(line) > 2 and line not in seen_lines:
                combined_text += line + '\n'
                seen_lines.add(line)
    
    # Если результат пустой, проба более агрессивных настройек
    if not combined_text.strip():
        # Попробуем с разными PSM режимами
        psm_modes = ['--psm 3', '--psm 4', '--psm 6', '--psm 8', '--psm 11']
        for psm in psm_modes:
            try:
                fallback_text = pytesseract.image_to_string(gray, lang='rus+eng', config=psm)
                if fallback_text.strip():
                    combined_text = fallback_text
                    break
            except:
                continue
    
    return combined_text.strip()

def extract_text_from_uploaded_file(file_path, file_type):
    if file_type == 'pdf':
        return extract_text_from_pdf(file_path)
    else:  # image
        return extract_text_from_image(file_path)