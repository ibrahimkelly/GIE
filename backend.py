# -*- coding: utf-8 -*-
"""
Created on Tue Dec 01 08:00:00 2020

@author: Ibrahim Kelly
@contact: hello99world99@gmail.com
"""

import sqlite3

class DataBase:
    def __init__(self):
        self.connection = sqlite3.connect("BaseDeDonnee.db")
        self.curseur = self.connection.cursor()

        database_tables = """CREATE TABLE IF NOT EXISTS employees
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT NULL,
            prenom BLOB(19) NULL,
            surnom BLOB(19) NULL,
            nom BLOB(19) NULL,
            date_entrer DATETIME,
            date_debut DATETIME,
            salaire INTEGER,
            id_dette INTEGER,
            total_dette INTEGER,
            epargne INTEGER,
            prenom_tuteur BLOB(19),
            nom_tuteur BLOB(19),
            telephone_tuteur INTEGER,
            adresse_tuteur BLOB(19)
        );

        CREATE TABLE IF NOT EXISTS paiements
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT NULL,
            id_employee INTEGER,
            ANNEE INTEGER NULL,
            JANVIER INTEGER NULL DEFAULT 0,
            FEVRIER INTEGER NULL DEFAULT 0,
            MARS INTEGER NULL DEFAULT 0,
            AVRIL INTEGER NULL DEFAULT 0,
            MAI INTEGER NULL DEFAULT 0,
            JUIN INTEGER NULL DEFAULT 0,
            JUILLET INTEGER NULL DEFAULT 0,
            AOUT INTEGER NULL DEFAULT 0,
            SEPTEMBRE INTEGER NULL DEFAULT 0,
            OCTOBRE INTEGER NULL DEFAULT 0,
            NOVEMBRE INTEGER NULL DEFAULT 0,
            DECEMBRE INTEGER NULL DEFAULT 0,
            FOREIGN KEY(id_employee) REFERENCES employees(id)
        );

        CREATE TABLE IF NOT EXISTS DETTE
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT NULL,
            id_employee INTEGER,
            MONTANT INTEGER DEFAULT 0
        );
        """

        self.curseur.executescript(database_tables)
        self.connection.commit()
        print("Great...")

if __name__ == "__main__":
    backend = DataBase()