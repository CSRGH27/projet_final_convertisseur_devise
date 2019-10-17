from PySide2 import QtWidgets
import currency_converter

# Tres important , Des qune instance est cree la methode init est execute
# ON cree nos differentes methode pour ensuite les execute dans notre methode init()
# Attention a l'ordre des methodes


class App(QtWidgets.QWidget):  # On cree une classe enfant App() de la classe parent QWidget()
    def __init__(self):
        super().__init__()    # On recupere le fonction init de la classe parent avec super
        # ON cree une instance de la classe CurrencyConverter()
        self.c = currency_converter.CurrencyConverter()
        self.setWindowTitle("Convertisseur de devises")
        self.setup_css()
        self.setup_ui()
        self.set_default_values()
        self.setup_connections()

    # Creation de l'interface,on va creer une methode pour ca (layout des widget, menu deroulant,bouton...)

    def setup_ui(self):
        # layout vertical avec QhBoxLayout()
        self.layout = QtWidgets.QHBoxLayout(self)
        # Creation d'une comboBox pour rentrer la valeur qu'on veut convertir
        self.cbb_devisesFrom = QtWidgets.QComboBox()
        self.spn_montant = QtWidgets.QSpinBox()
        # Un combobox pour la valeur final
        self.cbb_devisesTo = QtWidgets.QComboBox()
        self.spn_montantConverti = QtWidgets.QSpinBox()
        self.btn_inverser = QtWidgets.QPushButton("Inverser devises")

        # On ajoute les widget au layout
        self.layout.addWidget(self.cbb_devisesFrom)
        self.layout.addWidget(self.spn_montant)
        self.layout.addWidget(self.cbb_devisesTo)
        self.layout.addWidget(self.spn_montantConverti)
        self.layout.addWidget(self.btn_inverser)

    # ON definir les valeur
    def set_default_values(self):
        # On fait apparaitre das la combobox une liste trie des monnaies
        self.cbb_devisesFrom.addItems(sorted(list(self.c.currencies)))
        self.cbb_devisesTo.addItems(sorted(list(self.c.currencies)))
        # ON definit les valeurs par defaut dan les combobox
        self.cbb_devisesFrom.setCurrentText("EUR")
        self.cbb_devisesTo.setCurrentText("HUF")

        # On definit le range des valeurs min max
        self.spn_montant.setRange(1, 1000000000)
        self.spn_montantConverti.setRange(1, 1000000000)
        # On va definir la valeur des spinBox
        self.spn_montant.setValue(100)
        self.spn_montantConverti.setValue(100)

    def setup_connections(self):
        # On connecte les widget des qu'on les utilise aux methodes, par exemple des que la valeur change on active la fonction compute() commme onChange onClick
        self.cbb_devisesFrom.activated.connect(self.compute)
        self.cbb_devisesTo.activated.connect(self.compute)
        self.spn_montant.valueChanged.connect(self.compute)
        self.btn_inverser.clicked.connect(self.inverser_devise)
    # Modifictaion style

    def setup_css(self):
        self.setStyleSheet("""
        background-color: rgb(30, 30, 30);
        color: rgb(240, 240, 240);
        border:"none";
        width:150px;
        """)

    def compute(self):
        # ON recupere le montant rentre
        montant = self.spn_montant.value()
        # on recupere les devises
        devise_from = self.cbb_devisesFrom.currentText()
        devise_to = self.cbb_devisesTo.currentText()
        # On recupere le resulat de la convertion avec le module currency_converter
        # Avec le try on gere l'erreur si la conversion n'est ps trouve
        try:
            resultat = self.c.convert(montant, devise_from, devise_to)
        except currency_converter.currency_converter.RateNotFoundError:
            print("La conversion n'a pas fonctionne.")
        else:  # Si il n'y a pas d'erreur on lance cette coomande
            self.spn_montantConverti.setValue(resultat)

    def inverser_devise(self):
        devise_from = self.cbb_devisesFrom.currentText()
        devise_to = self.cbb_devisesTo.currentText()

        self.cbb_devisesFrom.setCurrentText(devise_to)
        self.cbb_devisesTo.setCurrentText(devise_from)

        self.compute()


app = QtWidgets.QApplication([])  # Creation de l'application
win = App()  # ON cree la fenetre avec l'instance win de la classe App()
win.show()  # On affiche la fenetre

app.exec_()  # On execute l'application
