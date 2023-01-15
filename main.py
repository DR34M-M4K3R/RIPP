import tkinter as tk
from tkinter import ttk
import sqlite3
from database import db
import random
import uuid
cellules=[]

def updateTable():

    db.afficherDb()
    try:
        vide.grid_forget()

    except Exception as e:
        print(e)

    for text in cellules:
        text.grid_forget()


    my_conn = sqlite3.connect('database.db')
    cursor = my_conn.cursor()
    r_set=my_conn.execute('''SELECT * from contacts''');
    testtt=cursor.fetchall()
    rows = 9
    i=0
    columns = 5

    my_conn = sqlite3.connect('database.db')
    r_set=my_conn.execute('''SELECT * from contacts''');
     # row value inside the loop
    for contact in r_set:
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


    # Set the canvas scrolling region
    canvas.config(scrollregion=canvas.bbox("all"))



def ajout():
    """
    Si la commande ci-dessous est placée directement dans la création du boutton, elle s'execute dès l'assignement de ce dernier.
    Il est alors nécéssaire de créer une fonction tièrce.
    """
    id = uuid.uuid4().hex
    id = id[:5]
    id = str(id )
    db.NouveauContact(id, nomEntry.get(), prenomEntry.get(), numeroEntry.get(), emailEntry.get())


def suppr():
    db.SupprContact(supprEntry.get())
    supprEntry.delete(0, tk.END)
    updateTable()




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


frame_canvas = tk.Frame(frame_main)
frame_canvas.grid(row=2, column=0, columnspan=5, rowspan=9, pady=(5, 0), sticky='nw')
frame_canvas.grid_rowconfigure(0, weight=1)
frame_canvas.grid_columnconfigure(0, weight=1)
frame_canvas.grid_propagate(False)

# Add a canvas in that frame
canvas = tk.Canvas(frame_canvas, bg="white")
canvas.grid(row=0, column=0, sticky="news")

# Link a scrollbar to the canvas
vsb = ttk.Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)

vsb.grid(row=0, column=1, sticky='ns')
canvas.configure(yscrollcommand=vsb.set)

# Frame qui contient les cellules
frame_cellules = tk.Frame(canvas, bg="red")
canvas.create_window((0, 0), window=frame_cellules, anchor='nw')


vide = tk.Label(frame_main, text="Aucun contacts. Ajoutez-en via les entrées à droite.", height=1, bg='white', fg='black')


tk.Label(frame_main, text="Id", width=11, bg='white', fg='black', borderwidth=2).grid(row=0, column=0)
tk.Label(frame_main, text="Nom", width=11, bg='white', fg='black', borderwidth=2).grid(row=0, column=1)
tk.Label(frame_main, text="Prénom", width=11, bg='white', fg='black', borderwidth=2).grid(row=0, column=3)
tk.Label(frame_main, text="Numéro", width=11, bg='white', fg='black', borderwidth=2).grid(row=0, column=2)
tk.Label(frame_main, text="Email", width=11, bg='white', fg='black', borderwidth=2).grid(row=0, column=4)



#tk.Label(frame_main, text="Rechercher", width=11, bg='white', fg='black', borderwidth=2).grid(row=1, column=6)
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


rechercheButton = tk.Button(frame_main, text="Rechercher", bg='white', fg='black', command=lambda:[ajout(), updateTable()])
rechercheButton.grid(row=4, column=8)


ajoutButton = tk.Button(frame_main, text="Ajouter", bg='white', fg='black', command=lambda:[ajout(), updateTable()])
ajoutButton.grid(row=4, column=9)


tk.Label(frame_main, text="Id", width=5, bg='white', fg='black', borderwidth=2).grid(row=6, column=8)

supprEntry = tk.Entry(frame_main, width=11, bg='white', fg='black')
supprEntry.grid(row=7, column=8)

supprButton = tk.Button(frame_main, text="Supprimer", bg='white', fg='black', command=lambda:[suppr(), updateTable()])
supprButton.grid(row=7, column=9)


updateTable()
# Launch the GUI
root.mainloop()
