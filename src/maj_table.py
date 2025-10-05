import duckdb
from settings import BASE_DE_DONNEES

def membre_present(con, nom_membre): 
    result = con.execute(f"""SELECT * from membres where membre = '{nom_membre}'""").fetchall()
    return True if result else False

def insert_membre(con , nom_membre): 
    con.execute(f"""
    INSERT INTO membres VALUES ('{nom_membre}', 0, 1, 0, 0)          
    """)

def maj_membre(con , nom_membre): 
    con.execute(f"""
    UPDATE membres SET absences = absences + 1 WHERE membre = '{nom_membre}'
    """)

def contenu_table(con): 
    result_liste = con.execute("""SELECT * from membres""").fetchall()
    result_table  = con.execute("""SELECT * from membres""").df()
    return result_liste, result_table


con = duckdb.connect(BASE_DE_DONNEES)
membre = 'test1'
if not membre_present(con, membre): 
    insert_membre(con, membre)
    print(f'membre {membre} inséré')
else: 
    print(f'membre {membre} déjà présent')

print(contenu_table(con)[0])
print(contenu_table(con)[1])