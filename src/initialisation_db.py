import duckdb
from settings import BASE_DE_DONNEES

# Connexion à une base locale (fichier duckdb)
con = duckdb.connect(BASE_DE_DONNEES)

# Création de la table si elle n'existe pas
con.execute("""
CREATE TABLE IF NOT EXISTS membres (
    membre TEXT,
    absences INTEGER,
    boosts INTEGER,
    helirace INTEGER,
    gemmes INTEGER
)
""")


con.close()
