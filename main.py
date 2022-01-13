import time

from kivy.metrics import dp

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
                ("SALAIRE", dp(24)),
                ("DATE DEBUT", dp(24)),
                ("PRENOM TUTEUR", dp(24)),
                ("NOM TUTEUR", dp(24)),
                ("QUARTIER", dp(24)),
                ("TELEPHONE", dp(24)),
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

    def getUserInfosForPaiement(self, ID):
        userID = ID
        if (userID == "" or userID.isnumeric()==False):
            self.ids["pUserName"].text = ""
            self.ids.idForPaiement.text = ''
            self.hideButton()
            self.clearPaiement()
        else:
            userID = backend.getEmployeeById(ID)[0]
            if (userID != []):
                print(userID)
                self.ids["pUserName"].text = f"[b]{userID[1]} {userID[2]} {userID[3]}[/b]"
                if (len(str(self.ids["year"].text)) == 4):
                    ID = self.ids["idForPaiement"].text
                    year = self.ids["year"].text
                    self.table = backend.getPaiementYear(ID, year)
                    print('Table : ', self.table)
                    if (self.table == []):
                        self.clearPaiement()
                        self.ids["addYear"].text = "[b]Ajouter[/b]"
                        self.ids["addYear"].bind(
                            on_press=lambda x: self.insertIntoMois(ID, year)
                        )
                    else:
                        print(len(self.table[0]))
                        #for i in range(len(self.table[0])):  # Code slow for about 2.20 seconds
                            #self.ids[self.MONTH[i]].text = str(self.table[0][i])
                else:
                    self.hideButton()
                    for i in range(len(self.MONTH)):
                        self.ids[self.MONTH[i]].text = ""
            else:
                self.ids["pUserName"].text = ""
                self.hideButton()

    def updatePaiement(self, id: int, year: int, mois: str, salaire: int) -> None:
        backend.updatePaiement(id, year, mois, salaire)

    def hideButton(self):
        self.ids["addYear"].text = ""
        self.ids["addYear"].bind(
            on_press=lambda x: None
        )

    def insertIntoMois(self, ID, year):
        backend.insertPaiement(ID, year)
        self.hideButton()

    def updateSomme(self, ID):
        try:
            userID = ID
            if (userID == "" or userID.isnumeric()==False):
                pass
            else:
                backend.updateTotal(userID)
                infos = self.getUpdateTotal(userID)
                dette = self.getSommeDette(userID)
                # To avoid soustraction with None error...
                infos = 0 if infos[0][0] is None else infos[0][0]  # print("Infos is different to none and numbers...")
                # To avoid soustraction with None error...
                if (dette[0][0] == "" or dette[0][0] == None):
                    dette = 0
                else:
                    dette = dette[0][0]  # print("Dette is different to none and numbers...")
                # To avoid soustraction with str error...
                # dette = 0 if dette[0][0] is '' else dette[0][0]
                self.ids["paiementInfos"].text = f"[b]Total des paiements : [color=#ffff00]{infos} F[/color][/b]"
                self.ids[
                    "paiementDetteInfos"].text = f"[b]Total de dettes accordées : [color=#ffff00]{dette} F[/color][/b]"
                self.ids[
                    "paiementCaisseInfos"].text = f"[b]Total restant : [color=#ffff00]{infos - dette} F[/color][/b]"

                if (len(str(self.ids["year"].text)) != 4):
                    self.ids["paiementInfos"].text = ""
                    self.ids["paiementInfos"].text = ""
                    self.ids["paiementDetteInfos"].text = ""
                    self.ids["paiementCaisseInfos"].text = ""
        except (IndexError, TypeError):
            # Pour les identifiants non dans la base de donnée,
            # Empeche l'ecriture dans les cases textuelles
            self.clearPaiement()

    def clearPaiement(self):
        for textInput in Body.MONTH:
            self.ids[textInput].text = ""
        self.ids["paiementInfos"].text = ""
        self.ids["paiementDetteInfos"].text = ""
        self.ids["paiementCaisseInfos"].text = ""

    def getUpdateTotal(self, id):
        userID = id
        result = str()
        if (userID == ""):
            pass
        else:
            result = backend.getUpdateTotal(userID)
        return result

#================================Dette==========================================

    def getUserInfosForDette(self, ID: int):
        userID = ID
        if (userID=="" or userID.isnumeric()==False):
            self.clearDette()
        else:
            userID = backend.DataBase.getEmployeeByID(ID)
            if (userID!=[]):
                self.ids["dUserName"].text = f"[b]{userID[0][0]} {userID[0][1]} {userID[0][2]}[/b]"
            else:
                self.ids["dUserName"].text = ""
                self.ids["detteMontant"].text = ""

    def setDette(self, ID):
        userID = self.ids["idForDette"].text
        montant = self.montantDette.text
        userInfos = str()
        if (userID==""):
            self.ids["detteInfos"].text = "[color=#ffff00]Aucun(e) employée trouvée...[/color]"
            Clock.schedule_once(self.hideDetteInfos, 3)
        elif (userID.isnumeric()==False):
            self.clearDette()
        else:
            userInfos = backend.DataBase.getEmployeeByID(userID)
            if (userID=="" or userInfos==[]):
                self.ids["detteInfos"].text = "[color=#ffff00]Aucun(e) employée trouvée...[/color]"
                Clock.schedule_once(self.hideDetteInfos, 3)
            elif (userID!="" and montant.isnumeric() and userInfos!=[]):

                if (int(montant)<1000 or int(montant)>=1000000):
                    self.ids["detteInfos"].text = "[color=#ffff00]Montant n'est pas dans la fourchette...[/color]"
                    Clock.schedule_once(self.hideDetteInfos, 3)
                else:
                    backend.DataBase.setDette(userID, montant)
                    self.updateSommeDette(userID)
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
            backend.DataBase.updateSommeDette(userID)
    
    def getSommeDette(self, ID):
        userID = ID
        result = ""
        if (userID==""):
            pass
        else:
            result = backend.DataBase.getSommeDette(userID)
        return result

    def clearDette(self):
        self.ids["idForDette"].text = ""
        self.ids["dUserName"].text = ""
        self.ids["detteMontant"].text = ""
    
    def hideDetteInfos(self, instence):
        self.ids["detteInfos"].text = ""

#================================Update==========================================

    def getUserInfosForUpdate(self, ID: int):

        userID = ID

        self.update_ids = [
            "updatePrenom", "updateSurnom", "updateNom",
            "updateSalaire", "updateDateEntrer","UpdateDateSortir",
            "updatePrenomTuteur", "updateNomTutuer", "updateTuteurContact",
            "updateAdressTuteur"
        ]

        if (userID=="" or userID.isnumeric()==False):
            self.ids.idToUpdate.text = ''
            self.cancelUpdate()
        else:
            userID = backend.DataBase.getEmployeeByID(ID)
            if (userID!=[]):
                self.ids["updatePrenom"].text = str(userID[0][0])
                self.ids["updateSurnom"].text = str(userID[0][1])
                self.ids["updateNom"].text = str(userID[0][2])

                self.ids["updateDateEntrer"].text = str(userID[1][0])
                self.ids["UpdateDateSortir"].text = str(userID[1][1])
                self.ids["updateSalaire"].text = str(userID[1][2])

                self.ids["updatePrenomTuteur"].text = str(userID[2][0])
                self.ids["updateNomTutuer"].text = str(userID[2][1])
                self.ids["updateTuteurContact"].text = str(userID[2][2])
                self.ids["updateAdressTuteur"].text = str(userID[2][3])
                
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
    
    def on_save(self, instance, value, date_range):
        self.ids.updateDateEntrer.text = str(value)

    def on_cancel(self, instance, value):
        '''Events called when the "CANCEL" dialog box button is clicked.'''

    def show_date_picker(self):
        date_dialog = MDDatePicker() # max_date=datetime.datetime.now(); primary_color=app.theme_cls.primary_color
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()

    def clearUpdateID(self):
        self.ids["idToUpdate"].text = ""
        self.cancelUpdate()

    def setUpdate(self, ID):
        userID = ID
        if (userID==""):
            self.ids["updateInfos"].text = "[color=#ffff00]Veuillez entrer un identifiant...[/color]"
            Clock.schedule_once(self.hideUpdateInfos, 3)
        else:
            prenom, surnom, nom = (
                self.ids["updatePrenom"].text,
                self.ids["updateSurnom"].text,
                self.ids["updateNom"].text
            )
            date_in, date_out, salaire = (
                self.ids["updateDateEntrer"].text,
                self.ids["UpdateDateSortir"].text,
                self.ids["updateSalaire"].text
            )
            t_prenom, t_nom, t_contact, t_adress = (
                self.ids["updatePrenomTuteur"].text,
                self.ids["updateNomTutuer"].text,
                self.ids["updateTuteurContact"].text,
                self.ids["updateAdressTuteur"].text
            )
            backend.DataBase.setUpdate(
                userID, prenom, surnom, nom,
                date_in, date_out, salaire,
                t_prenom, t_nom, t_contact, t_adress
            )
            Clock.schedule_once(self.updateSuccess, 1.3)

    def updateSuccess(self, event):
        self.cancelUpdate()
        self.ids["idToUpdate"].text = ""
        self.ids["updateInfos"].text = "[color=#00ff00]Mise en jour effectuée...[/color]"
        Clock.schedule_once(self.hideUpdateInfos, 3)

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