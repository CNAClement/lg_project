import os
import cv2
import numpy as np
from traitement_image import image_to_data, extraire_bornes, ecrire_crop
from inference_input import classifier_crop
from settings import INPUT_DIR , CROPS_DIR, OUTPUT_DIR


os.makedirs(CROPS_DIR, exist_ok=True)
images_input = [image for image in os.listdir(INPUT_DIR) if image.lower().endswith((".png",".jpg",".jpeg"))]
print(f"liste des images à traiter dans {INPUT_DIR} : {images_input}    ")
for image in images_input:
    print(f"Traitement de {image}")
    if not os.path.exists(INPUT_DIR / image):
        print(f"Le fichier {image} n'existe pas dans le répertoire {INPUT_DIR}.")
        continue
    image_origine = cv2.imread(INPUT_DIR / image, cv2.IMREAD_GRAYSCALE)
    # image reconstruite (noir = 0)
    image_reconstruite = np.zeros_like(image_origine)
    print(INPUT_DIR / image)
    try : 
        data = image_to_data(INPUT_DIR / image)
    except Exception as e:
        print(f"Erreur lors du chargement de l'image : {e}")
        exit(1)
    

    for i, text in enumerate(data["text"]):
        if not text.strip():
            continue
        x, y, w, h = extraire_bornes(i, data)
        crop = image_origine[y:y+h, x:x+w]
        ecrire_crop(image, i , crop)
        prediction = classifier_crop(CROPS_DIR / f"{image}_crop_{i}.png")[0]
        if prediction == 1 :
            image_reconstruite[y:y+h, x:x+w] = image_origine[y:y+h, x:x+w]
    cv2.imwrite(OUTPUT_DIR / f"{image}_reconstruite.png", image_reconstruite)

