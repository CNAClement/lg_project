"""
A partir de l'image reconstruite (sans bruit, grâce au modèle de classification), 
on extrait le texte avec Tesseract et on le traite pour récupérer les informations d'intérêt : 
pseudo, montant boost, puissance, puis on teste si la puissance est nulle 
et si le boost est faible ou au contraire remarquable"""

import os
from traitement_image import image_to_text
from maj_table import maj_table_main
from settings import OUTPUT_DIR, IMAGES_TRAITEES_DIR


def detection_puissance_nulle(puissance) : 
    puissance_effective = puissance.split('/')[0] # on ne garde que la partie avant le /
    puissance_effective = puissance_effective[0:-1] # enlever le K final
    return puissance_effective == '0'

def detection_boost_faible(montant_boost) :
    return montant_boost < 1000

def detection_boost_remarquable(montant_boost) :
    return montant_boost > 4000



def regles_gestion_texte(texte) :
    """Traite le texte extrait de l'image reconstruite.
    Repère les membres qui n'ont pas participé, les boosts faibles et remarquables.
    Dans un premier temps : extrait les pseudos, les boosts et les puissances des différents joueurs,
    puis compare ces valeurs à des valeurs de référence."""
    for ligne in texte.split('\n'):
        print(f"- {ligne}") 
        for mot in ligne.split():
            print(f"  - {mot}")

    for ligne in texte.split('\n'):
        if not ligne.strip() or ligne.isspace() : 
            continue  # ignorer les lignes videss
        valeurs_interet = [mot for mot in ligne.split()] 
        # normalement, produit des listes de longueur 3 : pseudo, montant boost, puissance
        if len(valeurs_interet) != 3:
            print(f"Attention, il y a sûrement un problème avec la ligne '{ligne}'")
        else:
            pseudo, montant_boost, puissance = valeurs_interet
            montant_boost = int(montant_boost)
            print(f"Pseudo : {pseudo}, montant boost : {montant_boost}, puissance : {puissance}")


        if detection_puissance_nulle(puissance):
            print("Le membre n'a pas joué")
            maj_table_main(pseudo, 'maj_absences')

        elif detection_boost_faible(montant_boost):
            print("Le boost est faible.")
            maj_table_main(pseudo, 'boost_insuffisant')
        elif detection_boost_remarquable(montant_boost):
            print("Le boost est remarquable.")
            maj_table_main(pseudo, 'boost_remarquable')
        else:
            print("Le membre a joué avec un boost dans la moyenne.")


liste_images_input = [image for image in os.listdir(OUTPUT_DIR) if image.lower().endswith("reconstruite.png")]
print(f"liste des images à traiter dans {OUTPUT_DIR} : {liste_images_input}    ")

for image in liste_images_input :
    print(f"Traitement de {image}")
    texte = image_to_text(OUTPUT_DIR / image)
    print(texte)
    try : 
        regles_gestion_texte(texte)
    except Exception as e:
        print(f"Erreur lors du l'application des règles de gestion (débug : probablement lors de la maj de la table : {e}")
        exit(1)
    # déplacer le fichier dans un répertoire "images_traitees"
    os.makedirs(IMAGES_TRAITEES_DIR, exist_ok=True)
    os.rename(OUTPUT_DIR / image, IMAGES_TRAITEES_DIR / image)
    print(f"Image {image} déplacée dans {IMAGES_TRAITEES_DIR}")