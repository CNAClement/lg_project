import pandas as pd
import os
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.metrics import classification_report
import joblib
from settings import LABELS_CSV , CROPS_DIR_ENTRAINEMENT, modele_serialisé
from traitement_image import prétraitement_image


# Charger les labels
labels_df = pd.read_csv(LABELS_CSV)

x, y = [], []

for _, row in labels_df.iterrows():
    """On récupère toutes les images qui ont été labellisées (donc présentes dans le csv)
      et on va les chercher dans le répertoire."""
    # on parcourt le df ligne par ligne, row représente une série pandas (pd.Series), c’est-à-dire une ligne entière du tableau.
    img_path = os.path.join(CROPS_DIR_ENTRAINEMENT, row["nom_image"])
    if os.path.exists(img_path):
        print(f"On traite {row['nom_image']} (de label {row['label']})")
        x_crop = prétraitement_image(img_path) # shape (4096,)
        x.append(x_crop) # liste d'array de longueur 4096 . x = [array([0, 255, 127, ...]), array([12, 98, 4, ...]), ...]


        y.append(1 if row["label"] == "texte" else 0)
    else : 
        print(f"Image manquante : {img_path}")

print(f"x : {len(x)} éléments, y : {len(y)} éléments")

# pas vraiment utile car scikit-learn gère implicitement ça, mais au moins c'est explicite.
# on obtient un tableau numpy de shape (nb_images, 4096).
x = np.array(x)
y = np.array(y)

print(x) 

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
clf = svm.SVC(kernel='rbf', probability=True)
print(f"x_train : {len(x_train)} éléments, y_train : {len(y_train)} éléments")

clf.fit(x_train, y_train)

print(classification_report(y_test, clf.predict(x_test)))
joblib.dump(clf, modele_serialisé)
