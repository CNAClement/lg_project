import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.metrics import classification_report
import joblib
from settings import LABELS_CSV , CROPS_DIR, modele_serialisé
from pre_traitement_image import pre_traitement_image


# Charger les labels
labels_df = pd.read_csv(LABELS_CSV)

X, y = [], []

for _, row in labels_df.iterrows():
    """On récupère toutes les images qui ont été labellisées (donc présentes dans le csv)
      et on va les chercher dans le répertoire."""
    # on parcourt le df ligne par ligne, row représente une série pandas (pd.Series), c’est-à-dire une ligne entière du tableau.
    img_path = os.path.join(CROPS_DIR, row["nom_image"])
    if os.path.exists(img_path):
        print(f"On traite {img_path} (de label {row['label']})")
        x_crop = pre_traitement_image(img_path)
        y.append(1 if row["label"] == "texte" else 0)


X_train, X_test, y_train, y_test = train_test_split(x_crop, y, test_size=0.2, random_state=42)
clf = svm.SVC(kernel='rbf', probability=True)
clf.fit(X_train, y_train)

print(classification_report(y_test, clf.predict(X_test)))
joblib.dump(clf, modele_serialisé)
