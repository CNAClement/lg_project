"""Script qui n'st à lancer qu'une seule fois."""

import duckdb
from settings import BASE_DE_DONNEES

# Connexion à une base locale (fichier duckdb)
con = duckdb.connect(BASE_DE_DONNEES)

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
