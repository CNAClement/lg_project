import streamlit as st
from pathlib import Path
import pandas as pd
from PIL import Image
from settings import CROPS_DIR_ENTRAINEMENT, LABELS_CSV

print("Ce script doit être lancé avec : streamlit run streamlit_etiquettage_pour_entrainement.py")
# Configuration de la page
st.set_page_config(page_title="Étiquetage d'images", layout="centered")

# --- Config ---
# CROPS_FOLDER : répertoire d'entrée (output de extraire_contours.py)
# LABELS_CSV = fichier de sortie 

# --- Charger les images ---
image_paths = sorted(Path(CROPS_DIR_ENTRAINEMENT).glob("*.png"))
print(f"image_paths: {image_paths}")

if not image_paths:
    st.error(f"Aucune image trouvée dans {CROPS_DIR_ENTRAINEMENT}")
    st.stop()

# --- Charger labels existants ---
if Path(LABELS_CSV).exists():
    df_labels = pd.read_csv(LABELS_CSV)
else:
    df_labels = pd.DataFrame(columns=["nom_image", "label"])

# --- Gestion de l'état Streamlit ---
if "index" not in st.session_state:
    st.session_state.index = 0

# S'assurer que l'index est dans les limites
if st.session_state.index >= len(image_paths):
    st.session_state.index = len(image_paths) - 1

# --- Image courante ---
current_image_path = image_paths[st.session_state.index]
current_image_name = current_image_path.name

# --- Affichage des informations ---
st.title("🏷️ Étiquetage d'images - v2")
st.write(f"Image {st.session_state.index + 1} sur {len(image_paths)}")

# Barre de progression
progress = (st.session_state.index + 1) / len(image_paths)
st.progress(progress)

# --- Affichage image ---
try:
    image = Image.open(current_image_path)
    st.image(image, caption=current_image_name, width='content' ) 
    # anciennement use_container_width=False   
    # #Please replace `use_container_width` with `width`
    # `use_container_width` will be removed after 2025-12-31.
    #  For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
except Exception as e:
    st.error(f"Erreur lors du chargement de l'image : {e}")
    st.stop()

# --- Récupérer le label existant s'il existe ---
existing_label = None
if not df_labels.empty and current_image_name in df_labels['nom_image'].values:
    existing_label = df_labels[df_labels.nom_image == current_image_name]['label'].iloc[0]

# --- Choix label avec valeur par défaut ---
labels_options = ("texte", "icône")
default_index = 0
if existing_label and existing_label in labels_options:
    default_index = labels_options.index(existing_label)

label = st.radio(
    "Choisir le label :", 
    labels_options,
    index=default_index,
    key=f"radio_{st.session_state.index}"  # Clé unique pour éviter les conflits
)

# --- Affichage du statut ---
if existing_label:
    st.info(f"🏷️ Label existant : **{existing_label}**")

# --- Boutons de navigation ---
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("⬅️ Précédent", disabled=(st.session_state.index == 0)):
        st.session_state.index -= 1
        st.rerun()

with col2:
    if st.button("💾 Sauvegarder"):
        # Sauvegarder le label actuel
        df_labels = df_labels[df_labels.nom_image != current_image_name]  # supprime ligne existante
        new_row = pd.DataFrame({"nom_image": [current_image_name], "label": [label]})
        df_labels = pd.concat([df_labels, new_row], ignore_index=True)
        df_labels.to_csv(LABELS_CSV, index=False)
        st.success(f"✅ Label '{label}' sauvegardé pour {current_image_name}")

with col3:
    if st.button("➡️ Suivant"):
        # Sauvegarder automatiquement avant de passer au suivant
        df_labels = df_labels[df_labels.nom_image != current_image_name]  # supprime ligne existante
        new_row = pd.DataFrame({"nom_image": [current_image_name], "label": [label]})
        df_labels = pd.concat([df_labels, new_row], ignore_index=True)
        df_labels.to_csv(LABELS_CSV, index=False)
        
        # Passer à l'image suivante
        if st.session_state.index + 1 < len(image_paths):
            st.session_state.index += 1
            st.rerun()  # Force le rechargement de la page
        else:
            st.success("🎉 Toutes les images ont été étiquetées !")

# --- Affichage du résumé ---
if not df_labels.empty:
    st.sidebar.header("📊 Résumé des labels")
    label_counts = df_labels['label'].value_counts()
    st.sidebar.write(label_counts)
    
    # Pourcentage de completion
    labeled_count = len(df_labels)
    total_count = len(image_paths)
    completion = (labeled_count / total_count) * 100 if total_count > 0 else 0
    st.sidebar.metric("Progression", f"{labeled_count}/{total_count}", f"{completion:.1f}%")
