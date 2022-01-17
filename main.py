import datetime
import time

from kivy.metrics import dp
from kivymd.uix.button import MDFillRoundFlatIconButton, MDIconButton, MDRectangleFlatIconButton

import backend
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.animation import Animation
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.picker import MDDatePicker
from kivymd.uix.datatables import MDDataTable

backend = backend.DataBase()

class Body(MDBoxLayout):

    """
    enreg_infos and enreg_inputs are used to cancel enregstrement...
    """

    prenom = ObjectProperty(None)
    surnom = ObjectProperty(None)
    nom = ObjectProperty(None)

    montantDette = ObjectProperty(None)
    montantPaiement = ObjectProperty(None)
    dataTableContainer = ObjectProperty(None)

    paiementYear = ObjectProperty(None)
    pToolbar = ObjectProperty(None)

    MONTH = [
        "janvier", "fevrier", "mars", "avril",
        "mai", "juin", "juillet", "aout",
        "septembre", "octobre", "novembre", "decembre"
    ]

    def __init__(self, **kwargs):
        super(Body, self).__init__(**kwargs)

        self.data_tables = MDDataTable(
            use_pagination=True,
            column_data=[
                ("ID", dp(19)),
                ("PRENOM", dp(24)),
                ("SURNOM", dp(24)),
                ("NOM", dp(24)),
                ("ENTRER", dp(24)),
                ("SALAIRE", dp(24)),
                ("PAIEMENTS", dp(24)),
                ("DETTES", dp(24)),
                ("EPARGNE", dp(24))
            ],
            elevation=19
        )

    def check_enreg_error(self):

        if self.prenom.text=='' or self.prenom.text.isalpha()==False or len(self.prenom.text)>13:
            self.prenom.helper_text = 'Veuillez renseigner un prénom correct...'
            self.prenom.error = True
        else:
            self.prenom.helper_text, self.prenom.error = '', False

        if (len(self.surnom.text)>13):
            self.surnom.helper_text = 'Veuillez renseigner un surnom correct...'
            self.surnom.error = True
        else:
            self.surnom.helper_text, self.surnom.error = '', False

        if (self.nom.text=='' or self.nom.text.isalpha()==False or len(self.nom.text)<2):
            self.nom.helper_text = 'Veuillez renseigner un nom correct...'
            self.nom.error = True
        else:
            self.nom.helper_text, self.nom.error = '', False

    def saveRecords(self):

        prenomValue = self.prenom.text.capitalize()
        surnomValue = self.surnom.text.capitalize()
        nomValue = self.nom.text.capitalize()

        # By default textFields error mode is set to False, so this methode is called to check their contents
        self.check_enreg_error()

        if (self.prenom.error==False and self.surnom.error==False and self.nom.error==False):
            if (backend.checEmployeeExistence(prenomValue, surnomValue, nomValue)==True):
                self.ids["enreg_infos"].text = "[color=#ffff00]Ce nom existe déjà dans la base de donnée...[/color]"
                Clock.schedule_once(self.hideInfo, 3)
            else:
                backend.saveEmployee(prenomValue, surnomValue, nomValue)
                self.clearEnregInput()
                self.ids["enreg_infos"].text = "[color=#00ff00]Enregistrement réussi...[/color]"
                Clock.schedule_once(self.hideInfo, 3)
        else:
            self.ids["enreg_infos"].text = "[color=#ffff00]Veuillez renseigner correctement les informations...[/color]"
            Clock.schedule_once(self.hideInfo, 3)

    def cancelEnregistrement(self):
        self.clearEnregInput()
        self.ids['enreg_infos'].text = "[color=#ffff00]Enregistrement annulé[/color]"
        Clock.schedule_once(self.hideInfo, 3)

    def clearEnregInput(self):
        self.prenom.text, self.prenom.error = '', False
        self.surnom.text, self.surnom.error = '', False
        self.nom.text, self.nom.error = '', False

    def hideInfo(self, event):
        self.ids["enreg_infos"].text = ""
    
    def hideTitle(self):
        self.animation = Animation(size=(self.size[0], 0), t="in_quad")
        self.animation.start(self.ids["title"])
    
    def showTitle(self):
        self.animation = Animation(size=(self.size[0], 64), t="in_quad")
        self.animation.start(self.ids["title"])

#================================Employees==========================================

    def showEmployeesList(self, filtre: str):
        nom = filtre.capitalize()
        employees_list = backend.getEmployeesByNom(nom)
        self.dataTableContainer.clear_widgets()
        self.data_tables.row_data = employees_list
        self.data_tables.bind(on_row_press=self.on_row_press)
        self.dataTableContainer.add_widget(self.data_tables)

    def on_row_press(self, instance_table, instance_row):
        '''Called when a table row is clicked.'''

        print(instance_table, instance_row)

    # ================================Paiement==========================================

    def getUserInfosForPaiement(self, id: int):

        try: # if id not found in the database, the foundUser = backend.getEmployeeById(id)[0] will raise an IndexError
            if (id == "" or id.isnumeric()==False):
                self.ids["pUserName"].text = ""
                self.ids.idForPaiement.text = ''
                self.hideButton()
                self.clearPaiement()
            else:
                foundUser = backend.getEmployeeById(id)[0]
                if (foundUser != []):
                    self.ids["pUserName"].text = f"[b]{foundUser[1]} {foundUser[2]} {foundUser[3]}[/b]"
                    if (len(str(self.paiementYear.text)) == 4):
                        id = self.ids["idForPaiement"].text
                        self.table = backend.getYearPaiement(id, self.paiementYear.text)
                        if (self.table == []):
                            self.clearPaiement()
                            self.addYearButton = MDFillRoundFlatIconButton(
                                icon='plus',
                                text='Ajouter',
                                font_size=dp(24),
                                on_press=lambda x: self.addNewYear(id)
                            )
                            self.pToolbar.add_widget(self.addYearButton)
                        else:
                            for i in range(len(self.table[0])-4): # Code slow for about 2.20 seconds
                                self.ids[self.MONTH[i]].text = str(self.table[0][i+3])
                    else:
                        self.hideButton()
                        for i in range(len(self.MONTH)):
                            self.ids[self.MONTH[i]].text = ""
                else:
                    self.hideButton()
        except(IndexError):
            self.ids["pUserName"].text = f"[color=#ff0][b]Aucun employé (e) trouvée avec l'id : {id}[/b][/color]"

    def updatePaiement(self, id: int, year: int, mois: str, salaire: int) -> None:
        backend.updatePaiement(id, year, mois, salaire)

    def hideButton(self):
        self.pToolbar.remove_widget(self.addYearButton)

    def addNewYear(self, id: int):
        check_year_existence = backend.checkAnneeExistence(id, self.paiementYear.text)
        if (check_year_existence):
            pass
        else:
            backend.insertPaiement(id, self.paiementYear.text)
            self.hideButton()

    def updateSomme(self, id: int):
        if (id == "" or id.isnumeric()==False):
            pass
        else:
            backend.updateTotal(id, self.paiementYear.text)
            backend.updateTotalPaiement(id)
            backend.updateEpargne(id)
            total_paiement = self.getUpdateTotal(id, self.paiementYear.text)
            total_paiement = 0 if total_paiement is None else total_paiement
            self.ids["total_paiement"].text = f"[b]Total des paiements : [color=#ffff00]{total_paiement} F[/color][/b]"

            if (len(str(self.paiementYear.text)) != 4):
                self.ids["total_paiement"].text = ""

    def clearPaiement(self):
        for textInput in Body.MONTH:
            self.ids[textInput].text = ""
        self.ids["total_paiement"].text = ""

    def getUpdateTotal(self, id, annee: int):
        result = str()
        if (id == "" or annee.isnumeric()==False):
            pass
        else:
            result = backend.getUpdateTotal(id, annee)
        return result

    def updateEpargne(self, id: int) -> None:
        backend.updateEpargne(id)

#================================Dette==========================================

    def getUserInfosForDette(self, id: int):
        if (id=="" or id.isnumeric()==False):
            self.clearDette()
        else:
            foundUser = backend.getEmployeeById(id)
            if (foundUser!=[]):
                self.ids["dUserName"].text = f"[b]{foundUser[0][1]} {foundUser[0][2]} {foundUser[0][3]}[/b]"
            else:
                self.ids["dUserName"].text = ""
                self.ids["detteMontant"].text = ""

    def setDette(self, id: int):
        montant = self.montantDette.text
        if (id=="" or id.isnumeric()==False):
            self.ids["detteInfos"].text = "[color=#ffff00]Aucun(e) employée trouvée...[/color]"
            Clock.schedule_once(self.hideDetteInfos, 3)
        elif (id.isnumeric()==False):
            self.clearDette()
        else:
            foundUser = backend.getEmployeeById(id)
            if (foundUser=="" or foundUser==[]):
                self.ids["detteInfos"].text = "[color=#ffff00]Aucun(e) employée trouvée...[/color]"
                Clock.schedule_once(self.hideDetteInfos, 3)
            elif (id!="" and montant.isnumeric() and foundUser!=[]):

                if (int(montant)<1000 or int(montant)>=1000000):
                    self.ids["detteInfos"].text = "[color=#ffff00]Montant n'est pas dans la fourchette...[/color]"
                    Clock.schedule_once(self.hideDetteInfos, 3)
                else:
                    date = datetime.datetime.now()
                    backend.insertDette(id, date, montant)
                    self.updateEpargne(id)
                    self.updateSommeDette(id)
                    self.clearDette()
                    self.ids["detteInfos"].text = "[color=#00ff00]Dette accorder avec succès...[/color]"
                    Clock.schedule_once(self.hideDetteInfos, 3)

            else:
                self.ids["detteInfos"].text = "[color=#ffff00]Montant invalide...[/color]"
                Clock.schedule_once(self.hideDetteInfos, 3)

    def updateSommeDette(self, ID):
        userID = ID
        if (userID=="" or userID.isnumeric()==False):
            pass
        else:
            backend.updateTotalDette(userID)
    
    def getSommeDette(self, id: int):
        result = ""
        if (id=="" or id.isnumeric()==False):
            pass
        else:
            result = backend.getTotalDette(id)
        return result

    def clearDette(self):
        self.ids["idForDette"].text = ""
        self.ids["dUserName"].text = ""
        self.ids["detteMontant"].text = ""
    
    def hideDetteInfos(self, instence):
        self.ids["detteInfos"].text = ""

#================================Update==========================================

    def getUserInfosForUpdate(self, id: int):

        self.update_ids = [
            "updatePrenom", "updateSurnom", "updateNom",
            "updateSalaire", "updateDateEntrer", "updateDateDebut",
            "updatePrenomTuteur", "updateNomTutuer", "updateTuteurContact",
            "updateAdressTuteur"
        ]

        if (id=="" or id.isnumeric()==False):
            self.ids.idToUpdate.text = ''
            self.cancelUpdate()
        else:
            foundUser = backend.getUserForUpdate(id)
            if (foundUser!=[]):
                self.ids["updatePrenom"].text = str(foundUser[0][0])
                self.ids["updateSurnom"].text = str(foundUser[0][1])
                self.ids["updateNom"].text = str(foundUser[0][2])

                self.ids["updateDateEntrer"].text = str(foundUser[0][3])
                self.ids["updateSalaire"].text = str(foundUser[0][4])
                self.ids["updateDateDebut"].text = str(foundUser[0][5])

                self.ids["updatePrenomTuteur"].text = str(foundUser[0][6])
                self.ids["updateNomTutuer"].text = str(foundUser[0][7])
                self.ids["updateTuteurContact"].text = str(foundUser[0][8])
                self.ids["updateAdressTuteur"].text = str(foundUser[0][9])

                self.ids["updateInfos"].text = ""
            else:
                self.ids["updateInfos"].theme_text_color = "Custom"
                self.ids["updateInfos"].text_color = (1, 1, 0, 1)
                self.ids["updateInfos"].text = "Aucun resultat..."
                self.cancelUpdate()
                Clock.schedule_once(self.hideUpdateInfos, 3)
    
    def hideUpdateInfos(self, instence):
        self.ids["updateInfos"].text = ""

    def cancelUpdate(self):
        try:
            for ids in self.update_ids:
                self.ids[ids].text = ""
        except AttributeError:
            pass
    
    def setEnterDate(self, instance, value, date_range):
        self.ids.updateDateEntrer.text = str(value)

    def setStartDate(self, instance, value, date_range):
        self.ids.updateDateDebut.text = str(value)

    def on_cancel(self, instance, value):
        '''Events called when the "CANCEL" dialog box button is clicked.'''

    def shooseEnterDate(self):
        date_dialog = MDDatePicker() # max_date=datetime.datetime.now(); primary_color=app.theme_cls.primary_color
        date_dialog.bind(on_save=self.setEnterDate, on_cancel=self.on_cancel)
        date_dialog.open()

    def shooseStartDate(self):
        date_dialog = MDDatePicker() # max_date=datetime.datetime.now(); primary_color=app.theme_cls.primary_color
        date_dialog.bind(on_save=self.setStartDate, on_cancel=self.on_cancel)
        date_dialog.open()

    def clearUpdateID(self):
        self.ids["idToUpdate"].text = ""
        self.cancelUpdate()

    def setUpdate(self, id: int):
        if (id=="" or id.isnumeric()==False):
            self.ids["updateInfos"].text = "[color=#ffff00]Veuillez entrer un identifiant...[/color]"
            Clock.schedule_once(self.hideUpdateInfos, 3)
        else:
            prenom, surnom, nom = (
                self.ids["updatePrenom"].text,
                self.ids["updateSurnom"].text,
                self.ids["updateNom"].text
            )
            date_in, date_start, salaire = (
                self.ids["updateDateEntrer"].text,
                self.ids["updateDateDebut"].text,
                self.ids["updateSalaire"].text
            )
            t_prenom, t_nom, t_contact, t_adress = (
                self.ids["updatePrenomTuteur"].text,
                self.ids["updateNomTutuer"].text,
                self.ids["updateTuteurContact"].text,
                self.ids["updateAdressTuteur"].text
            )
            backend.updateEmployee(
                id, prenom, surnom, nom,
                date_in, date_start, salaire,
                t_prenom, t_nom, t_contact, t_adress
            )
            Clock.schedule_once(self.updateSuccess, 0.8)

    def updateSuccess(self, event):
        self.cancelUpdate()
        self.ids["idToUpdate"].text = ""
        self.ids["updateInfos"].text = "[color=#00ff00]Mise en jour effectuée...[/color]"
        Clock.schedule_once(self.hideUpdateInfos, 1.9)

class Icontent(MDBoxLayout):
    pass

class Main(MDApp):

    title = "GIE"

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        return Body()

if __name__=="__main__":
    Main().run()