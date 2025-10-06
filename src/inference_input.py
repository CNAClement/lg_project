"""Reçoit un crop et le classifie.
Cela permettra dans un autre script de reconstruire une image en ne gardant que les crops 
identifiés comme du texte et de remplacer les autres par des carrés noirs."""

import joblib
from traitement_image import prétraitement_image
from settings import modele_serialisé

modele_classifieur = joblib.load(modele_serialisé)

def classifier_crop(crop_path):
    """Classifie un crop en texte ou icône"""
    x_crop = prétraitement_image(crop_path) # shape (4096,)
    x_crop = x_crop.reshape(1, -1) # reshape pour avoir la bonne forme (1, 4096)
    # rappel, pour son entrainement, le modèle prend en entrée un x qui est un tableau numpy 2D de shape (nb_images, 4096)


    prediction = modele_classifieur.predict(x_crop)
    proba = modele_classifieur.predict_proba(x_crop)

    # modele_classifieur.predict(x_crop) ==> renvoie une liste de même taille que le nombre d'images à analyser
    # dans le cas de l'inférence : on n'analyse qu'une image à la fois donc on ne récupère qu'une valeur

    return prediction[0], proba[0]



