from pathlib import Path
print(f"Si un jour ce path imprime /workspaces, on pourra se passer de la variable WORKSPACE :\n{ Path.home()}")
WORKSPACE = Path("/workspaces/lg_inactifs")
INPUT_DIR = WORKSPACE / "input"
TRAVAIL_DIR = WORKSPACE / "travail"
OUTPUT_DIR = WORKSPACE / "output"
DEBUG_DIR = WORKSPACE / "debug"
IMAGES_TRAITEES_DIR = OUTPUT_DIR / "images_traitées"
CROPS_DIR = TRAVAIL_DIR / "crops_raw"
CROPS_DIR_ENTRAINEMENT = TRAVAIL_DIR / "crops_training"
LABELS_CSV = TRAVAIL_DIR / "labels.csv"
BASE_DE_DONNEES = WORKSPACE / "lg_inactifs.duckdb"
modele_serialisé = OUTPUT_DIR / "classification_texte_vs_icone.pkl"
MODE_DEBUG = True