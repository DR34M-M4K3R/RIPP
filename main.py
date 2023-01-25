import tkinter as tk
from tkinter import ttk
import sqlite3
from database import db
import random
import uuid
import os
cellules=[]


def searchContact():

    """
    Permet d'appliquer des filtres à l'affichage de la base de donnée.

    Cette fonction trouve les contacts qui possèdent un ou plusieurs attributs entrés dans les champs de texte
    et lance la mise à jour des cellules avec la liste des contacts.
    """
    my_conn = sqlite3.connect('database.db')
    cursor = my_conn.cursor()
    data=my_conn.execute('''SELECT * FROM contacts ORDER BY nom''');

    log(f"Obtention des éléments possédant ces valeurs:{nomEntry.get()}, {prenomEntry.get()}, {numeroEntry.get()}, {emailEntry.get()}")
    dataList=list(data)
    searchResult=[]
    for i in range(len(dataList)):
        for j in range(len(dataList[i])):
            if dataList[i][j] == nomEntry.get() or dataList[i][j] == prenomEntry.get() or dataList[i][j] == numeroEntry.get() or dataList[i][j] == emailEntry.get():
                searchResult.append(dataList[i])
                print("\n",dataList[i])


    updateTable(searchResult)



def updateTable(*args):

    """
    Met a jour les cellules du tableau (texte et taille).

    La fonction vérifie si un argument est passé ou non.
    Si c'est le cas, elle affiche le tableau qui est passé en argument.
    Sinon, c'est la base de donnée entière qui est affichée par défaut.

    """


    log("Mise à jour des cellules avec les valeurs de la bdd...")

    if len(args)==0:
        log("Mise à jour des cellules avec les valeurs de la bdd...")
        my_conn = sqlite3.connect('database.db')
        cursor = my_conn.cursor()
        dataSet=my_conn.execute('''SELECT * FROM contacts ORDER BY nom''')



    else:
        log("Mise à jour des cellules avec les valeurs de la recherche...")
        dataSet=args
        dataSetTest=[]
        for contact in dataSet:
            for j in contact:
                dataSetTest.append(j)
        dataSet=dataSetTest
        print(dataSet)

    db.afficherDb()
    try:
        vide.grid_forget()

    except Exception as e:
        print(e)

    for text in cellules:
        text.grid_forget()



    rows = 9
    i=0
    columns = 5
    # on affiche les cellules
    for contact in dataSet:
        for j in range(len(contact)):
            c = tk.Text(frame_cellules, width=17, height=1, bg='white', fg='black')
            c.insert(tk.END, contact[j])
            #c.configure(state='disabled')
            c.grid(row=i, column=j, sticky='news')
            cellules.append(c)
        i=i+1


    # Calculer la taille des cellules
    frame_cellules.update_idletasks()

    try:
        first5rows_height = sum([cellules[i].winfo_height() for i in range(0, 5)])+200

        first5columns_width = sum([cellules[i].winfo_width() for j in range(0, 5)])

        frame_canvas.config(width=vsb.winfo_width()+first5columns_width, height=first5rows_height)
    except Exception as e:
        print("Table vide.")

        vide.grid(row=7, column=1)

    canvas.config(scrollregion=canvas.bbox("all"))
    nomEntry.delete(0, tk.END)
    prenomEntry.delete(0, tk.END)
    numeroEntry.delete(0, tk.END)
    emailEntry.delete(0, tk.END)



def deleteDatabase():
    """
    Supprime le fichier contenant la base de donnée.
    """
    os.remove("database.db")

def log(text):
    """
    Affiche le texte passé comme argument dans l'espace de log
    """
    displayedText=f"\n[*] {text}"
    logTextBox.insert(tk.END, displayedText)
    logTextBox.yview_moveto(1) # scroller jusqu'en bas

def ajout():
    """
    -Bug?-: Si la commande ci-dessous est placée directement dans la création du boutton, alors elle s'execute dès l'assignement de ce dernier.
    Il est alors nécéssaire de créer une fonction tièrce.
    """


    id = uuid.uuid4().hex
    id = id[:3]
    id = str(id)
    log(f"Ajout de l'élément: {id}, {nomEntry.get().title()}, {prenomEntry.get().title()}, {numeroEntry.get()}, {emailEntry.get()}")
    db.NouveauContact(id, nomEntry.get().title(), prenomEntry.get().title(), numeroEntry.get(), emailEntry.get())


def suppr():
    """
    Demande au module db.py la suppression d'un contact et met à jour l'affichage.
    """
    log(f"Suppression de l'élément avec l'id {supprEntry.get()}")

    db.SupprContact(supprEntry.get())
    supprEntry.delete(0, tk.END)
    #updateTable()



db.CreateDB()
db.afficherDb()

root = tk.Tk()
root.grid_rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
root.geometry("1200x600")


style=ttk.Style()
style.theme_use('classic')
style.configure("Vertical.TScrollbar", background="grey", arrowcolor="white")

frame_main = tk.Frame(root, bg="white")
frame_main.grid(sticky='news')

logTextBox = tk.Text(frame_main, width=75, height=7, bg='#dadada', fg='black')
logTextBox.config(spacing1=12)
logTextBox.insert(tk.END, "--- Start log ---")
logTextBox.grid(row=20, column=0, columnspan=6)

# Creation de la frame qui va contenir le canvas
frame_canvas = tk.Frame(frame_main)
frame_canvas.grid(row=2, column=0, columnspan=5, rowspan=10, pady=(5, 0), sticky='nw')
frame_canvas.grid_rowconfigure(0, weight=1)
frame_canvas.grid_columnconfigure(0, weight=1)
frame_canvas.grid_propagate(False)

# Ajout du canvas a la frame
canvas = tk.Canvas(frame_canvas, bg="white")
canvas.grid(row=0, column=0, sticky="news")

# Ajout d'une scrollbar
vsb = ttk.Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
vsb.grid(row=0, column=1, sticky='ns')
canvas.configure(yscrollcommand=vsb.set)

# Creation de la frame qui contient les cellules
frame_cellules = tk.Frame(canvas, bg="red")
canvas.create_window((0, 0), window=frame_cellules, anchor='nw')

vide = tk.Label(frame_main, text="Aucun contacts. Ajoutez-en via les entrées à droite.", height=1, bg='white', fg='black')

tk.Label(frame_main, text="Id", width=11, bg='white', fg='black', borderwidth=2).grid(row=0, column=0)
tk.Label(frame_main, text="Nom", width=11, bg='white', fg='black', borderwidth=2).grid(row=0, column=1)
tk.Label(frame_main, text="Prénom", width=11, bg='white', fg='black', borderwidth=2).grid(row=0, column=2)
tk.Label(frame_main, text="Numéro", width=11, bg='white', fg='black', borderwidth=2).grid(row=0, column=3)
tk.Label(frame_main, text="Email", width=11, bg='white', fg='black', borderwidth=2).grid(row=0, column=4)


tk.Label(frame_main, text="Nom", width=11, bg='white', fg='black', borderwidth=2).grid(row=2, column=7)
tk.Label(frame_main, text="Prénom", width=11, bg='white', fg='black', borderwidth=2).grid(row=2, column=8)
tk.Label(frame_main, text="Numéro", width=11, bg='white', fg='black', borderwidth=2).grid(row=2, column=9)
tk.Label(frame_main, text="Email", width=11, bg='white', fg='black', borderwidth=2).grid(row=2, column=10)


nomEntry = tk.Entry(frame_main, width=11, bg='white', fg='black')
nomEntry.grid(row=3, column=7)

prenomEntry = tk.Entry(frame_main, width=11, bg='white', fg='black')
prenomEntry.grid(row=3, column=8)

numeroEntry = tk.Entry(frame_main ,width=11, bg='white', fg='black')
numeroEntry.grid(row=3, column=9)

emailEntry = tk.Entry(frame_main, width=11, bg='white', fg='black')
emailEntry.grid(row=3, column=10)


rechercheButton = tk.Button(frame_main, text="Rechercher", bg='white', fg='black', command=searchContact)
rechercheButton.grid(row=4, column=8)


ajoutButton = tk.Button(frame_main, text="Ajouter", bg='white', fg='black', command=lambda:[ajout(), updateTable()])
ajoutButton.grid(row=4, column=9)

tk.Label(frame_main, text="Id", width=5, bg='white', fg='black', borderwidth=2).grid(row=6, column=8)

supprEntry = tk.Entry(frame_main, width=11, bg='white', fg='black')
supprEntry.grid(row=7, column=8)

supprButton = tk.Button(frame_main, text="Supprimer", bg='white', fg='black', command=lambda:[suppr(), updateTable()])
supprButton.grid(row=7, column=9)

updateButton = tk.Button(frame_main, text="Mettre à jour les cellules", bg='white', fg='black', command=updateTable).grid(row=15, column=7, columnspan=4)
updateButton = tk.Button(frame_main, text="Supprimer la base de donnée", bg='white', fg='black', command=deleteDatabase).grid(row=16, column=7, columnspan=4)



updateTable()

root.mainloop()
