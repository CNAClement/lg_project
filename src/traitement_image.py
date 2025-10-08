import cv2
from matplotlib import image
import pytesseract
from pytesseract import Output
import os
from settings import CROPS_DIR, MODE_DEBUG, TRAVAIL_DIR, DEBUG_DIR

def prétraitement_crop(image_path):
    if os.path.exists(image_path):
        # print(f"image trouvée : {image_path}")
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE) # gris pour atténuer le bruit
        image = cv2.resize(image, (64,64))  
        x_crop = image.flatten()
        return x_crop
    else:
        raise FileNotFoundError(f"L'image {image_path} n'existe pas.")

def prétraitement_image(image_path : str):
    """
    Prétraite une image pour Tesseract OCR avec affichage des étapes intermédiaires.
    Étapes :
      1. Lecture en niveaux de gris
      2. Denoising (flou gaussien)
      3. Égalisation du contraste
      4. Binarisation adaptative
      5. Morphologie (fermeture)
      6. Inversion éventuelle
    """
    # 1️) Lecture directe en niveaux de gris
    gray = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    if binary is None:
        raise ValueError(f"Erreur lors du chargement de l'image : {image_path}")

    # 2️) Réduction du bruit
    img_blur = cv2.GaussianBlur(binary, (3, 3), 0)

    # 3️) Amélioration du contraste
 
    # 4️) Binarisation adaptative (méthode de choix pour OCR sur fond non uniforme)
    img_bin = cv2.adaptiveThreshold(
        img_blur,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        35,
        11
    )

    # 5️) Morphologie (fermeture → comble les petits trous et relie les caractères disjoints)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    img_final = cv2.morphologyEx(img_bin, cv2.MORPH_CLOSE, kernel)

    if MODE_DEBUG:
        import matplotlib.pyplot as plt

        # 🔍 Visualisation des différentes étapes
        titles = [
            "1. Original (Grayscale)",
            "2. Gaussian Blur (Denoise)",
            "3. Equalized Histogram (Contrast)",
            "4. Adaptive Threshold (Binarization)",
            "5. Morphology (Closing)",
        ]
        images = [gray , binary, img_blur, img_bin, img_final]

        plt.figure(figsize=(15, 8))
        for i in range(5):
            plt.subplot(2, 3, i + 1)
            plt.imshow(images[i], cmap="gray")
            plt.title(titles[i], fontsize=10)
            plt.axis("off")
        plt.tight_layout()
        plt.savefig(DEBUG_DIR / f"debug_{image_path.stem}.png", dpi=150)
        plt.close()

    return img_final

    
def image_to_data(image_path): 
    """"Renvoie un dictionnaire avec : 
    left", "top", "width", "height" : les coordonnées des boîtes détectées
    "text" : le texte reconnu
    "conf" : la confiance associée à chaque détection"""
    image = prétraitement_image(image_path)
    custom_config = "--psm 6 --oem 3"
    data = pytesseract.image_to_data(image, config=custom_config, output_type=pytesseract.Output.DICT)
    if MODE_DEBUG:
        img_visu = draw_tesseract_boxes(image, data, min_conf=2)
        cv2.imwrite(TRAVAIL_DIR / F"debug_{image_path.stem}_tesseract_boxes.png", img_visu)
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

def draw_tesseract_boxes(image, data, min_conf=0):
    """
    Dessine les boîtes de détection de Tesseract sur l'image.
    
    Args:
        image: image OpenCV (np.array)
        data: dictionnaire retourné par pytesseract.image_to_data()
        min_conf: seuil minimal de confiance (0–100) pour afficher la boîte.
    """
    # Copie l'image originale pour ne pas la modifier directement
    img_visu = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    n_boxes = len(data["text"])
    for i in range(n_boxes):
        if int(data["conf"][i]) > min_conf and data["text"][i].strip() != "":
            (x, y, w, h) = (data["left"][i], data["top"][i], data["width"][i], data["height"][i])
            cv2.rectangle(img_visu, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(img_visu, data["text"][i], (x, y - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    return img_visu