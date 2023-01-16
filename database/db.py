import sqlite3, json

con = sqlite3.connect("database.db", check_same_thread=False)
cursor = con.cursor()


def CreateDB():
    cursor = con.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS contacts(id TEXT, nom TEXT, prenom TEXT, numero integer, email TEXT)")
    #cursor.execute("CREATE TABLE IF NOT EXISTS contacts(nom TEXT, prenom TEXT, numero integer, email TEXT)")

    con.commit()



def SupprContact(id):
    parameter = id
    cursor.execute("DELETE FROM contacts WHERE id = ?", (id,))
    con.commit()


def afficherDb():

    """
    Affiche les donnees de la base de donnees
    """

    # Display data
    print('\nData in contacts table:')
    data=cursor.execute('''SELECT * FROM contacts''')
    for row in data:
        print(row)


    con.commit()

def NouveauContact(id, nom, prenom, numero, email):
    parameters = (id, nom, prenom, numero, email)

    cursor.execute("INSERT INTO contacts(id, nom, prenom, numero, email) VALUES (?, ?, ?, ?, ?)", parameters)
    #cursor.execute(f"INSERT INTO contacts(nom, prenom, numero, email) VALUES ('{nom}', '{prenom}', '{numero}', '{email}')")
    con.commit()
