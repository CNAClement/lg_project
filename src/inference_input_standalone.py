"""Récupère le contenu de input, fais les crops puis appelle le modèle de classification
pour ne garder que les textes qui sont ensuite analysés par Tesseract.
Ne marche pas très bien, les crops ne sont pas bien traités car Tesseract manque de contexte global.
Le script inference_input.py traite les crops un à un pour reconstruire au préalable une image non bruitée."""

import os
import joblib
import numpy as np
from settings import modele_serialisé, CROPS_DIR
from traitement_image import image_to_text , prétraitement_crop

modele_classifieur = joblib.load(modele_serialisé)
liste_crops = [crop for crop in os.listdir(CROPS_DIR) if crop.lower().endswith(".png")]
liste_crops_prétraités = []
for crop in liste_crops : 
    crop_path = os.path.join(CROPS_DIR, crop)
    x_crop = prétraitement_crop(crop_path) # shape (4096,)
    liste_crops_prétraités.append(x_crop)
    # x_crop = x_crop.reshape(1, -1) # reshape pour avoir la bonne forme (1, 4096)
    # rappel, pour son entrainement, le modèle prend en entrée un x qui est un tableau numpy 2D de shape (nb_images, 4096)



x = np.array(liste_crops_prétraités)  # shape (nb_crops, 4096)
prediction = modele_classifieur.predict(x)
proba = modele_classifieur.predict_proba(x)

# modele_classifieur.predict(x_crop) ==> renvoie une liste de même taille que le nombre d'images à analyser


for crop, pred in zip(liste_crops, prediction):
    if pred == 1 :
        print(f"Crop : {crop}")
        crop_path = CROPS_DIR / crop
        texte = image_to_text(crop_path)
        print(texte)

