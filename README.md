Il s'agit d'un projet personnel, essentiellement à des fins d'entrainement et de plaisir personnel, qui me permet de pratiquer : 
- Docker 
- DevContainer (une surcouche qui permet de binder son workspace local vScode au conteneur)
- Du Machine Learning et différents outils (ex : Tesseract pour OCR)
- Streamlit
- DuckDB, qui est une base de donnée embarquée (un peu comme sqllite), facile à installer et à manipuler mais orientée analytique. Pas forcément extrêmement adaptée à mon cas d'usage mais le but reste de manipuler.

L'objectif du projet est de faciliter le suivi des inactifs et des plus faibles contributeurs dans un jeu auquel je joue. 

Dans ce jeu, on peut être membre d'une alliance et participer collectivement à une guerre contre d'autres alliances. 
Si on oublie de jouer, cela pénalise l'alliance (puisque les membres des alliances ennemies, eux, n'oublient pas de jouer et on se retrouve en infériorité numérique). 
Par ailleurs, on a la possibilité de dépenser des ressources personnelles pour le "bien commun", et on se retrouve évidemment avec des membres qui se sacrifient pour le bien de l'alliance, et inversement, des membres qui profitent plus qu'ils n'apportent.

On a accès à une interface qui nous dit chaque jour quel membre à fait quoi. Il s'agit d'une interface graphique (avec des icônes, etc). Je souhaite prendre des captures d'écran de ces interfaces et les placer dans le dossier /input, puis analyser (ML + OCR) le contenu de ces images, et enfin de mettre à jour une base de donnée synthétisant l'apport de chaque membre (compteur nombre de fois AFK, nombre de fois participation faible, etc.)

L'image étant très bruitée, je vais entrainer un modèle de classification qui permettra de faire la distinction entre les zones d'intérêt et le reste. 
Streamlit me permet de classifier tout ça rapidement : 
streamlit run streamlit_etiquettage_pour_entrainement.py 

Une fois que cette distinction a été faite, je reconstruis (au fur et à mesure) l'image initiale en remplaçant toutes les zones inutiles par du noir et en ne gardant que les zones d'intérêt, puis je traite l'image reconstruite avec Tesseract pour en extraire le texte sur lequel je vais travailler à partir de règles de gestion.


Cinématiques : 
Pour l'entrainement du modèle :
1) Lancer le script reconstruire_image_sans_bruit.py pour générer les crops, et en déplacer certains dans travail/crops_training pour faire un travail de labellisation à la main (ne pas prendre en compte l'image reconstruite générée dans /output si ce n'est pas pertinent.)
2) Labeliser les crops manuellement avec streamlit (streamlit run streamlit_etiquettage_pour_entrainement.py")
3) entrainer le modèle (script entrainement_classifieur.py)

Pour la prod
1) Lancer le script reconstruire_image_sans_bruit.py. Ce script génère les crops et utilise le modèle entrainé précédemment (via inference_inputs.py) pour reconstruire l'image finale à utiliser.
2) Lancer le script traitement_texte.py . Ce script traduit l'image finale en texte, puis applique certaines règles de gestion en fonction des valeurs détectées et met à jour la base de données (via maj_table.py)

Les images sont prétraitées avec pre_traitement_image.py (conversion en gris, rescale ...)