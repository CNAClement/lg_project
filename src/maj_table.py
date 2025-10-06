import duckdb
from settings import BASE_DE_DONNEES

def membre_present(con, nom_membre): 
    result = con.execute(f"""SELECT * from membres where membre = '{nom_membre}'""").fetchall()
    return True if result else False

def insert_membre(con , nom_membre): 
    con.execute(f"""
    INSERT INTO membres VALUES ('{nom_membre}', 0, 1, 0, 0)          
    """)

def maj_absences(con , nom_membre): 
    con.execute(f"""
    UPDATE membres SET absences = absences + 1 WHERE membre = '{nom_membre}'
    """)

def maj_boost(con , nom_membre , valeur): 
    con.execute(f"""
    UPDATE membres SET boosts = boosts + {valeur} WHERE membre = '{nom_membre}'
    """)


def contenu_table(con): 
    result_liste = con.execute("""SELECT * from membres""").fetchall()
    result_table  = con.execute("""SELECT * from membres""").df()
    return result_liste, result_table


def maj_table_main(membre, action): 
    con = duckdb.connect(BASE_DE_DONNEES)
    if not membre_present(con, membre): 
        insert_membre(con, membre)
        print(f'membre {membre} inséré')

    if action == 'maj_absences': 
        maj_absences(con, membre)
        print(f'membre {membre} mis à jour')
    elif action == 'boost_insuffisant': 
        maj_boost(con, membre, 1)
        print(f"maj boost insuffisant +1 pour {membre}")
    elif action == 'boost_remarquable' : 
        maj_boost(con, membre, - 2)
        print(f"maj boost remarquable -2 pour {membre}")


    print(contenu_table(con)[0])
    print(contenu_table(con)[1])