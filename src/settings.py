from pathlib import Path
print(f"Si un jour ce path imprime /workspaces, on pourra se passer de la variable WORKSPACE :\n{ Path.home()}")
WORKSPACE = Path("/workspaces/lg_inactifs")
INPUT_DIR = WORKSPACE / "input"
OUTPUT_INTERMEDIAIRE_DIR = WORKSPACE / "output"
CROPS_DIR = OUTPUT_INTERMEDIAIRE_DIR / "crops_raw"
CROPS_DIR_ENTRAINEMENT = OUTPUT_INTERMEDIAIRE_DIR / "crops_training"
LABELS_CSV = OUTPUT_INTERMEDIAIRE_DIR / "labels.csv"
IMG_PATH = INPUT_DIR / "1.png"
BASE_DE_DONNEES = WORKSPACE / "lg_inactifs.duckdb"
modele_serialisé = OUTPUT_INTERMEDIAIRE_DIR / "classification_texte_vs_icone.pkl"
