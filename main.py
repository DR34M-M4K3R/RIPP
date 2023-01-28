#!/usr/bin/env python3

from tkinter.filedialog import askopenfilename
from tkinter import ttk
import tkinter as tk
import sqlite3
import random
import uuid
import sys
import os


# -*- coding: utf-8 -*-


"""

Copyright © 2023 www.github.com/DR34M-M4K3R
Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the “Software”),
to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

"""

class app():

    def __init__(self, database_name):
            self.database_name=database_name
            self.cellules=[]
            self.myDb = db(database_name)
            #self.myDb.createDB(database_name)
            self.root = tk.Tk()
            photo = tk.PhotoImage(file="icone.png")
            self.root.iconphoto(False, photo)
            self.root.grid_rowconfigure(0, weight=1)
            self.root.columnconfigure(0, weight=1)
            self.root.geometry("1200x600")
            self.root.title("RIPP")



            style=ttk.Style()
            style.theme_use('classic')
            style.configure("Vertical.TScrollbar", background="grey", arrowcolor="white")

            frame_main = tk.Frame(self.root, bg="white")
            frame_main.grid(sticky='news')



            # Creation de la frame qui va contenir le canvas
            self.frame_canvas = tk.Frame(frame_main)
            self.frame_canvas.grid(row=2, column=0, columnspan=5, rowspan=10, pady=(5, 0), sticky='nw')
            self.frame_canvas.grid_rowconfigure(0, weight=1)
            self.frame_canvas.grid_columnconfigure(0, weight=1)
            self.frame_canvas.grid_propagate(False)

            # Ajout du canvas a la frame
            self.canvas = tk.Canvas(self.frame_canvas, bg="white")
            self.canvas.grid(row=0, column=0, sticky="news")

            # Ajout d'une scrollbar
            self.vsb = ttk.Scrollbar(self.frame_canvas, orient="vertical", command=self.canvas.yview)
            self.vsb.grid(row=0, column=1, sticky='ns')
            self.canvas.configure(yscrollcommand=self.vsb.set)

            # Creation de la frame qui contient les cellules
            self.frame_cellules = tk.Frame(self.canvas, bg="red")
            self.canvas.create_window((0, 0), window=self.frame_cellules, anchor='nw')

            self.first = tk.Label(frame_main, text="Aucun contacts. Ajoutez-en via les entrées à droite.", height=1, bg='white', fg='black')
            self.first.grid(row=7, column=1)



            tk.Label(frame_main, text="Id", width=11, bg='white', fg='black', borderwidth=2).grid(row=0, column=0)
            tk.Label(frame_main, text="Nom", width=11, bg='white', fg='black', borderwidth=2).grid(row=0, column=1)
            tk.Label(frame_main, text="Prénom", width=11, bg='white', fg='black', borderwidth=2).grid(row=0, column=2)
            tk.Label(frame_main, text="Numéro", width=11, bg='white', fg='black', borderwidth=2).grid(row=0, column=3)
            tk.Label(frame_main, text="Email", width=11, bg='white', fg='black', borderwidth=2).grid(row=0, column=4)

            tk.Label(frame_main, text="Nom", width=11, bg='white', fg='black', borderwidth=2).grid(row=2, column=7)
            tk.Label(frame_main, text="Prénom", width=11, bg='white', fg='black', borderwidth=2).grid(row=2, column=8)
            tk.Label(frame_main, text="Numéro", width=11, bg='white', fg='black', borderwidth=2).grid(row=2, column=9)
            tk.Label(frame_main, text="Email", width=11, bg='white', fg='black', borderwidth=2).grid(row=2, column=10)



            self.nomEntry = tk.Entry(frame_main, width=11, bg='white', fg='black')
            self.nomEntry.grid(row=3, column=7)

            self.prenomEntry = tk.Entry(frame_main, width=11, bg='white', fg='black')
            self.prenomEntry.grid(row=3, column=8)

            self.numeroEntry = tk.Entry(frame_main ,width=11, bg='white', fg='black')
            self.numeroEntry.grid(row=3, column=9)

            self.emailEntry = tk.Entry(frame_main, width=11, bg='white', fg='black')
            self.emailEntry.grid(row=3, column=10)

            tk.Label(frame_main, text="Id", width=5, bg='white', fg='black', borderwidth=2).grid(row=6, column=8)
            self.supprEntry = tk.Entry(frame_main, width=11, bg='white', fg='black')
            self.supprEntry.grid(row=7, column=8)




            rechercheButton = tk.Button(frame_main, text="Rechercher", bg='white', fg='black', activebackground='black', command=self.searchContact)
            rechercheButton.grid(row=4, column=8)

            ajoutButton = tk.Button(frame_main, text="Ajouter", bg='white', fg='green', activebackground='green', command=lambda:[self.ajout(), self.updateTable()])
            ajoutButton.grid(row=4, column=9)

            supprButton = tk.Button(frame_main, text="Supprimer", bg='white', fg='red', activebackground='red', command=lambda:[self.suppr(), self.updateTable()])
            supprButton.grid(row=7, column=9)

            updateButton = tk.Button(frame_main, text="Mettre à jour les cellules", bg='white', fg='black', activebackground='black', command=self.updateTable).grid(row=15, column=7, columnspan=4)
            deleteButton = tk.Button(frame_main, text="Supprimer la base de donnée", bg='white', fg='red', activebackground='red', command=self.deleteDatabase).grid(row=16, column=7, columnspan=4)
            quitButton = tk.Button(frame_main, text="Quitter", bg='white', fg='black', activebackground='red', command=quit).grid(row=17, column=7, columnspan=4)



            self.logTextBox = tk.Text(frame_main, width=75, height=7, bg='#dadada', fg='black')
            self.logTextBox.config(spacing1=12)
            self.logTextBox.insert(tk.END, "--- Start log ---")
            self.logTextBox.grid(row=16, column=0, columnspan=6, rowspan=5)


            self.updateTable()

            self.root.mainloop()



    def searchContact(self):

        """
        Permet d'appliquer des filtres à l'affichage de la base de donnée.

        Cette fonction trouve les contacts qui possèdent un ou plusieurs attributs entrés dans les champs de texte
        et lance la mise à jour des cellules avec la liste des contacts.
        """
        my_conn = sqlite3.connect(self.database_name)
        cursor = my_conn.cursor()
        data=my_conn.execute('''SELECT * FROM contacts ORDER BY nom''');

        self.log(f"Obtention des éléments possédant ces valeurs:{self.nomEntry.get()}, {self.prenomEntry.get()}, {self.numeroEntry.get()}, {self.emailEntry.get()}")
        dataList=list(data)
        searchResult=[]
        for i in range(len(dataList)):
            for j in range(len(dataList[i])):
                if dataList[i][j] == self.nomEntry.get() or dataList[i][j] == self.prenomEntry.get() or dataList[i][j] == self.numeroEntry.get() or dataList[i][j] == self.emailEntry.get():
                    searchResult.append(dataList[i])


        self.updateTable(searchResult)



    def updateTable(self, *args):

        """
        Met a jour les cellules du tableau (texte et taille).

        La fonction vérifie si un argument est passé ou non.
        Si c'est le cas, elle affiche le tableau qui est passé en argument.
        Sinon, c'est la base de donnée entière qui est affichée par défaut.

        """


        if len(args)==0:
            self.log("Mise à jour des cellules avec les valeurs de la bdd...")
            my_conn = sqlite3.connect(self.database_name)
            cursor = my_conn.cursor()
            dataSet=my_conn.execute('''SELECT * FROM contacts ORDER BY nom''')



        else:
            self.log("Mise à jour des cellules avec les valeurs de la recherche...")
            self.log(args)
            dataSet=args
            dataSetTest=[]
            for contact in dataSet:
                for j in contact:
                    dataSetTest.append(j)
            dataSet=dataSetTest

        try:
            self.noDataLabel.grid_forget()
        except Exception as e:
            pass



        # Reinitialisation des cellules
        for text in self.cellules:
            text.grid_forget()
        self.cellules=[]

        rows = 9
        i=0
        columns = 5
        # on affiche les cellules
        for contact in dataSet:
            for j in range(len(contact)):
                c = tk.Text(self.frame_cellules, width=17, height=1, bg='white', fg='black')
                c.insert(tk.END, contact[j])
                #c.configure(state='disabled')
                c.grid(row=i, column=j, sticky='news')
                self.cellules.append(c)
            i=i+1


        # Calculer la taille des cellules
        self.frame_cellules.update_idletasks()

        try:
            first5rows_height = sum([self.cellules[i].winfo_height() for i in range(0, 5)])+200
            first5columns_width = sum([self.cellules[i].winfo_width() for j in range(0, 5)])
            self.frame_canvas.config(width=self.vsb.winfo_width()+first5columns_width, height=first5rows_height)
        except Exception as e:
            self.noDataLabel = tk.Label(self.frame_cellules, text="Aucun contacts. Ajoutez-en via les entrées à droite.", height=1, bg='white', fg='black')
            self.noDataLabel.grid(row=7, column=1)

        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        self.nomEntry.delete(0, tk.END)
        self.prenomEntry.delete(0, tk.END)
        self.numeroEntry.delete(0, tk.END)
        self.emailEntry.delete(0, tk.END)

        if len(self.cellules)!=0:
            self.first.grid_forget()
        else:
            pass


    def deleteDatabase(self):
        """
        Supprime le fichier contenant la base de donnée.
        """
        self.log("Suppression de la base de donnée...")
        os.remove(self.database_name)
        self.root.destroy()



    def log(self, text):
        """
        Affiche le texte passé comme argument dans l'espace de log
        """
        displayedText=f"\n[*] {text}"
        self.logTextBox.insert(tk.END, displayedText)
        self.logTextBox.yview_moveto(1) # scroller jusqu'en bas

    def ajout(self):
        """
        -Bug?-: Si la commande ci-dessous est placée directement dans la création du boutton, alors elle s'execute dès l'assignement de ce dernier.
        Il est alors nécéssaire de créer une fonction tièrce.
        """

        try:
            self.first.grid_forget()
        except Exception as e:
            pass

        id = uuid.uuid4().hex
        id = id[:3]
        id = str(id)
        self.log(f"Ajout de l'élément: {id}, {self.nomEntry.get().title()}, {self.prenomEntry.get().title()}, {self.numeroEntry.get()}, {self.emailEntry.get()}")
        self.myDb.NouveauContact(id, self.nomEntry.get().title(), self.prenomEntry.get().title(), self.numeroEntry.get(), self.emailEntry.get())


    def suppr(self):
        """
        Demande a la classe la suppression d'un contact et met à jour l'affichage.
        """
        self.log(f"Suppression de l'élément avec l'id {self.supprEntry.get()}")

        self.myDb.SupprContact(self.supprEntry.get())
        self.supprEntry.delete(0, tk.END)
        #updateTable()




class db():

    def __init__(self, database_name):
        self.database_name=database_name

    def createDB(self):
        con = sqlite3.connect(self.database_name, check_same_thread=False)
        cursor = con.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS contacts(id TEXT, nom TEXT, prenom TEXT, numero integer, email TEXT)")
        con.commit()


    def SupprContact(self, id):
        con = sqlite3.connect(self.database_name, check_same_thread=False)
        cursor = con.cursor()
        parameter = id
        cursor.execute("DELETE FROM contacts WHERE id = ?", (id,))
        con.commit()


    def NouveauContact(self, id, nom, prenom, numero, email):
        con = sqlite3.connect(self.database_name, check_same_thread=False)
        cursor = con.cursor()
        parameters = (id, nom, prenom, numero, email)

        cursor.execute("INSERT INTO contacts(id, nom, prenom, numero, email) VALUES (?, ?, ?, ?, ?)", parameters)
        #cursor.execute(f"INSERT INTO contacts(nom, prenom, numero, email) VALUES ('{nom}', '{prenom}', '{numero}', '{email}')")
        con.commit()


class startupWindow():

    def __init__(self):
        self.file = ""
        filelist = [fname for fname in os.listdir('database/') if fname.endswith('.ripp')]

        self.master = tk.Tk()
        self.master.geometry('370x200')
        photo = tk.PhotoImage(file="icone.png")
        self.master.iconphoto(False, photo)
        self.master.grid_columnconfigure(4, minsize=100)


        content_frame = tk.Frame(self.master, bg="white")
        content_frame.pack(anchor=tk.N, fill=tk.BOTH, expand=True, side=tk.LEFT )
        self.master.title('RIPP | Choisissez ou créez un répertoire')


        self.optmenu = ttk.Combobox(content_frame, values=filelist, state='readonly')
        self.optmenu.grid(row=0, column=0, columnspan=2)


        tk.Button(content_frame, text="Ouvrir", bg='white', fg='black', command=self.getFile).grid(row=0, column=1, columnspan=4)
        tk.Button(content_frame, text="Nouvau Répertoire", bg='white', fg='black', command=self.newDb).grid(row=2, column=2)
        tk.Button(content_frame, text="Quitter", bg='white', fg='black', command=quit).grid(row=3, column=2)

        self.Entry = tk.Entry(content_frame, width=20, bg='white', fg='black')
        self.Entry.grid(row=2, column=0)

        tk.Label(content_frame, text=".ripp", height=1, bg='white', fg='black').grid(row=2, column=1)



        col_count, row_count = content_frame.grid_size()

        for col in range(col_count):
            content_frame.grid_columnconfigure(col, minsize=20)

        for row in range(row_count):
            content_frame.grid_rowconfigure(row, minsize=50)


        self.master.mainloop()


    def getFile(self):
        temp="database/"+self.optmenu.get()
        self.file=temp
        self.master.destroy()

    def newDb(self):
        temp="database/"+self.Entry.get()+".ripp"

        datab = db(temp)
        datab.createDB()
        self.file=temp
        self.master.destroy()



if __name__ == '__main__':
    while(True):
        startupWin = startupWindow()
        file=startupWin.file
        app(file)
