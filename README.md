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

L'image étant très bruitée, je vais entrainer un modèle qui permettra de faire la distinction entre les zones d'intérêt et le reste. 
Streamlit me permet de classifier tout ça rapidement : 
streamlit run streamlit_etiquettage_pour_entrainement.py 



Cinématique : 
1) lancer le script extraire_contours pour préparer les crops
2) labeliser les crops avec streamlit
3) entrainer le modèle
4) passer les crops reconnus comme "texte" par le modèle à Tesseract
5) utiliser les valeurs détectées par Tesseract pour mettre à jour la base de données

attention, la question va se poser de comment il relie chaque pseudo à chaque valeur (pour l'instant : traité indépendamment)