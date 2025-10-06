import cv2
import pytesseract
from pytesseract import Output
import os
from settings import INPUT_DIR , CROPS_DIR

def prétraitement_image(image_path):
    if os.path.exists(image_path):
        # print(f"image trouvée : {image_path}")
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE) # gris pour atténuer le bruit
        img = cv2.resize(img, (64,64))  
        x_crop = img.flatten()
        return x_crop
    else:
        raise FileNotFoundError(f"L'image {image_path} n'existe pas.")
    
def image_to_data(image): 
    img = cv2.imread(INPUT_DIR / image)
    data = pytesseract.image_to_data(img, output_type=Output.DICT)
    return data

def image_to_text(image_path):
    """Extrait le texte d'une image en utilisant Tesseract OCR."""
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"L'image {image_path} n'existe pas.")
    
    # Charger l’image
    img = cv2.imread(image_path)
    # Conversion en niveaux de gris
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Optionnel : binaire (contraste fort)
    _, thresh = cv2.threshold(gray, 190, 255, cv2.THRESH_BINARY)
    
    # OCR avec Tesseract
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(thresh, config=custom_config)

    return text

def extraire_bornes(i, data):
    x, y, w, h = data["left"][i], data["top"][i], data["width"][i], data["height"][i]
    return x, y, w, h

def ecrire_crop(image, i , crop):
    cv2.imwrite(CROPS_DIR / f"{image}_crop_{i}.png", crop)