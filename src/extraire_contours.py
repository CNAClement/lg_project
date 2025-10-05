import os
import cv2
import pytesseract
from pytesseract import Output
from settings import INPUT_DIR , CROPS_DIR


def extraire_contours():
    """
    Extrait les contours des zones de texte dans une image et sauvegarde les crops.
    
    Args:
        output (str): répertoire d'arrivée (crops_raw ou crops_training).
    """
    os.makedirs(CROPS_DIR, exist_ok=True)
    images_input = [image for image in os.listdir(INPUT_DIR) if image.lower().endswith((".png",".jpg",".jpeg"))]

    for image in images_input:
        print(f"Traitement de {image}"): 
        try :
            img = cv2.imread(INPUT_DIR / image)
        except Exception as e:
            print(f"Erreur lors du chargement de l'image : {e}")
            exit(1)

        data = pytesseract.image_to_data(img, output_type=Output.DICT)

    for i, text in enumerate(data["text"]):
        if not text.strip():
            continue
        x, y, w, h = data["left"][i], data["top"][i], data["width"][i], data["height"][i]
        crop = img[y:y+h, x:x+w]
        cv2.imwrite(os.path.join(CROPS_DIR, f"crop_{i}.png"), crop)
