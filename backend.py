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
            salaire INTEGER DEFAULT 0,
            total_dette INTEGER DEFAULT 0,
            epargne INTEGER DEFAULT 0,
            prenom_tuteur BLOB(19) DEFAULT NULL,
            nom_tuteur BLOB(19) DEFAULT NULL,
            telephone_tuteur INTEGER NULL,
            adresse_tuteur BLOB(19) DEFAULT NULL
        );

        CREATE TABLE IF NOT EXISTS paiements
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT NULL,
            id_employee INTEGER,
            annee INTEGER NULL,
            janvier INTEGER NULL DEFAULT 0,
            fevrier INTEGER NULL DEFAULT 0,
            mars INTEGER NULL DEFAULT 0,
            avril INTEGER NULL DEFAULT 0,
            mai INTEGER NULL DEFAULT 0,
            juin INTEGER NULL DEFAULT 0,
            juillet INTEGER NULL DEFAULT 0,
            aout INTEGER NULL DEFAULT 0,
            septembre INTEGER NULL DEFAULT 0,
            octobre INTEGER NULL DEFAULT 0,
            novembre INTEGER NULL DEFAULT 0,
            decembre INTEGER NULL DEFAULT 0,
            total INTEGER NULL DEFAULT 0,
            FOREIGN KEY(id_employee) REFERENCES employees(id)
        );

        CREATE TABLE IF NOT EXISTS dettes
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT NULL,
            id_employee INTEGER,
            date_credit DATETIME,
            montant INTEGER DEFAULT 0,
            FOREIGN KEY(id_employee) REFERENCES employees(id)
        );
        """

        self.curseur.executescript(database_tables)
        self.connection.commit()

    def saveEmployee(self, prenom: str, surnom: str, nom: str) -> None:
        query = """INSERT INTO employees('prenom', 'surnom', 'nom') VALUES(?, ?, ?)"""
        self.curseur.execute(query, (prenom, surnom, nom))
        self.connection.commit()

    def checEmployeeExistence(self, prenom: str, surnom: str, nom: str) -> bool:
        query = """SELECT * FROM employees WHERE prenom=? AND surnom=? AND nom=?"""
        self.curseur.execute(query, (prenom, surnom, nom))
        if (self.curseur.fetchall()):
            return True
        else:
            return False

    def updateEmployee(self):
        query = """"""
        self.curseur.execute()
        self.connection.commit()

    def getEmployeeById(self, id: int) -> list:
        query = """SELECT * FROM employees WHERE id=?"""
        self.curseur.execute(query, (id,))
        result = self.curseur.fetchall()
        return result

    def getEmployeesByNom(self, nom: str) -> list:
        query = """SELECT * FROM employees WHERE nom=?"""
        self.curseur.execute(query, (nom,))
        result = self.curseur.fetchall()
        return result

if __name__ == "__main__":
    backend = DataBase()