import cv2
import pytesseract
from settings import IMAGE_FOLDER

# Charger l’image
try :
    img = cv2.imread(f"{IMAGE_FOLDER}/1.png")
except Exception as e:
    print(f"Erreur lors du chargement de l'image : {e}")
    exit(1)

# Conversion en niveaux de gris
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Optionnel : binaire (contraste fort)
_, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

# OCR avec Tesseract
custom_config = r'--oem 3 --psm 6'
text = pytesseract.image_to_string(thresh, config=custom_config)

print("Texte brut OCR :")
print(text)
