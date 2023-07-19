from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox, QLabel, QFileDialog, QLineEdit
from PyQt6.QtGui import QIcon, QPixmap
from converter import Converter
from metadata_interface import MetadataWindow

class MainWindow(QMainWindow):
    """
    Trieda používateľského rozhrania hlavného okna aplikácie.
    """

    def __init__(self):
        """
        Inicializácia všetkých prvkov používateľského rozhrania aplikácie.
        """
        
        super(MainWindow, self).__init__()

        self.converter = Converter()

        self.setWindowTitle("RDF converter")
        self.setFixedWidth(450)
        self.setFixedHeight(350)

        self.converterLabel = QLabel()
        self.csvPixmap = QPixmap(self.converter.resource_path("csv2rdf.png"))
        self.rdfPixmap = QPixmap(self.converter.resource_path('rdf2csv.png'))      
        self.converterLabel.setPixmap(self.csvPixmap)
        
        #Input file
        self.inputLabel = QLabel("Vstupný (.csv) :")
        self.inputEdit = QLineEdit()
        self.inputEdit.textChanged.connect(self.inputChanged)
        self.inputFileButton = QPushButton()
        self.inputFileButton.clicked.connect(self.inputFileDialog)
        self.inputFileButton.setIcon(QIcon(self.converter.resource_path("folder.png")))

        #Output file      
        self.outputLabel = QLabel("Výstupný súbor (.ttl) :")
        self.outputEdit = QLineEdit()
        self.outputEdit.textChanged.connect(self.outputChanged)
        self.outputFileButton = QPushButton()
        self.outputFileButton.clicked.connect(self.outputFileDialog)
        self.outputFileButton.setIcon(QIcon(self.converter.resource_path("folder.png")))
        
        formatLabel = QLabel("Výstupný formát :") 
        self.formatComboBox = QComboBox()
        self.formatComboBox.addItems(["RDF/TTL", "RDF/XML"])
        self.formatComboBox.currentIndexChanged.connect(self.formatChanged)

        metadataButton = QPushButton("Čítať metadáta..")
        metadataButton.clicked.connect(self.readMetadata)
        self.addMetadataButton = QPushButton("Pridať metadáta")
        self.addMetadataButton.clicked.connect(self.openMetadataFileDialog)
        self.addMetadataButton.setIcon(QIcon(self.converter.resource_path("folder.png")))

        convertButton = QPushButton("Konverzia")
        convertButton.clicked.connect(self.convert)

        self.reverseButton = QPushButton()
        self.reverseButton.setCheckable(True)
        self.reverseButton.clicked.connect(self.checkChanged)
        self.reverseButton.setIcon(QIcon(self.converter.resource_path("reverse.png")))

        self.errorLabel = QLabel("")
        self.errorLabel.setStyleSheet("color: red; font-size: 14px;")
    
        labelLayout = QHBoxLayout()
        labelLayout.addStretch(3)
        labelLayout.addWidget(self.converterLabel)
        labelLayout.addWidget(self.reverseButton)
        labelLayout.addStretch(2)
        inputLayout = QHBoxLayout()
        inputLayout.addWidget(self.inputEdit)
        inputLayout.addWidget(self.inputFileButton)
        outputLayout = QHBoxLayout()
        outputLayout.addWidget(self.outputEdit)
        outputLayout.addWidget(self.outputFileButton)      
        formatLayout = QHBoxLayout()
        formatLayout.addWidget(self.formatComboBox)
        formatLayout.addWidget(self.addMetadataButton)
        formatLayout.addWidget(metadataButton)
        convertLayout = QHBoxLayout()
        convertLayout.addWidget(convertButton)

        layout = QVBoxLayout()
        layout.addLayout(labelLayout)
        layout.addWidget(self.inputLabel)
        layout.addLayout(inputLayout)
        layout.addStretch()
        layout.addWidget(self.outputLabel)
        layout.addLayout(outputLayout)
        layout.addWidget(formatLabel)
        layout.addLayout(formatLayout)
        layout.addLayout(convertLayout)
        layout.addWidget(self.errorLabel)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        widget.setStyleSheet("""
            QWidget {
                background-color: "#e8feff";
                font-size: 16px;
                color: "black";
            }
            QLabel {
                margin-left: 2px;
            }
            QComboBox {
                background: "#FFFFFF";
            }
            QLineEdit {
                background: "#FFFFFF";
            }
            QPushButton {
                font-size: 16px;
                padding: 6px 10px 6px 10px;
                margin: 5px 0px 5px 5px;
                background: #abddff;
                border: 1px solid rgb(66, 184, 221);
                border-radius: 6px;
            }
            QPushButton:hover {
                background: #8dc0e3;
            }
            QPushButton:checked {
                background: #5096c7;
            }
            QComboBox:disabled {
                color: "grey";
            }
        """)

    def inputFileDialog(self):
        """
        Dialógové okno výberu vstupného súboru.
        """

        fileDialog = QFileDialog()
        fileDialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        if not self.reverseButton.isChecked():
            fileDialog.setNameFilter("CSV súbor (*.csv)")
        else:
            fileDialog.setNameFilter("RDF súbor (*.ttl *.xml)")
        fileDialog.setViewMode(QFileDialog.ViewMode.List)
        if fileDialog.exec():
            self.csvPath = fileDialog.selectedFiles()[0]
            self.inputEdit.setText(fileDialog.selectedFiles()[0])
    
    def openMetadataFileDialog(self):
        """
        Dialógové okno výberu vstupného súboru metaúdajov.
        """

        if self.addMetadataButton.text() == "Pridať metadáta":
            fileDialog = QFileDialog()
            fileDialog.setFileMode(QFileDialog.FileMode.ExistingFile)
            fileDialog.setNameFilter("Súbor metadát (*.txt *.docx)")
            fileDialog.setViewMode(QFileDialog.ViewMode.List)
            if fileDialog.exec():
                self.converter.set_metadataPath(fileDialog.selectedFiles()[0])
                self.addMetadataButton.setText("Odstrániť metadáta")
                self.addMetadataButton.setIcon(QIcon())
        else:
            self.converter.set_metadataPath("")
            self.addMetadataButton.setText("Pridať metadáta")
            self.addMetadataButton.setIcon(QIcon(self.converter.resource_path("folder.png")))

    def readMetadata(self):
        """
        Spustenie používateľského rozhrania čítania metaúdajov.
        """

        self.dialog = MetadataWindow()
        self.dialog.show()


    def outputFileDialog(self):
        """
        Dialógové okno výberu výstupného súboru.
        """

        fileDialog = QFileDialog()
        fileDialog.setFileMode(QFileDialog.FileMode.AnyFile)
        if self.reverseButton.isChecked():
            fileDialog.setNameFilter("CSV súbor (*.csv)")
        elif self.converter.format == "ttl":
            fileDialog.setNameFilter("Turtle RDF súbor (*.ttl)")
        elif self.converter.format == "xml":
            fileDialog.setNameFilter("XML RDF súbor (*.xml)")

        fileDialog.setViewMode(QFileDialog.ViewMode.List)
        if fileDialog.exec():
            filePath = fileDialog.selectedFiles()[0]
            if self.reverseButton.isChecked():
                filePath = filePath.split(".")[0]+".csv"
            else:
                filePath = filePath.split(".")[0]+"."+self.converter.format

            self.outputEdit.setText(filePath)

    def inputChanged(self, path):
        """
        Pomocná funkcia pre zmenu vstupného súboru.
        """

        self.converter.set_inputPath(path)
        self.inputEdit.setStyleSheet("background: '#ffffff'")
        self.errorLabel.setText("")

    def outputChanged(self, path):
        """
        Pomocná funkcia pre zmenu výstupného súboru.
        """

        self.converter.set_outputPath(path)
        self.outputEdit.setStyleSheet("background: '#ffffff'")
        self.errorLabel.setText("")

    def formatChanged(self):
        """
        Pomocná funkcia pre zmenu formátu výstupného súboru.
        """

        if self.formatComboBox.currentText() == "RDF/XML" :
            self.converter.set_format("xml")
            self.outputLabel.setText("Výstupný súbor (.xml) :")
            if self.outputEdit.text() != "":
                fileName = self.outputEdit.text().split(".")
                self.outputEdit.setText(str(fileName[0])+".xml")
        elif self.formatComboBox.currentText() == "RDF/TTL":
            self.converter.set_format("ttl")
            self.outputLabel.setText("Výstupný súbor (.ttl) :")
            if self.outputEdit.text() != "":
                fileName = self.outputEdit.text().split(".")
                self.outputEdit.setText(str(fileName[0])+".ttl")

    def checkChanged(self):
        """
        Pomocná funkcia pre otočenie konverzie.
        """

        if (self.reverseButton.isChecked()):
            self.converterLabel.setPixmap(self.rdfPixmap)
            
            if self.outputEdit.text() != "":
                fileName = self.outputEdit.text().split(".")
                self.outputEdit.setText(str(fileName[0])+".csv")
            
            self.inputLabel.setText("Vstupný súbor (.ttl or .xml) :")
            self.outputLabel.setText("Výstupný súbor (.csv) :")
            
            self.formatComboBox.clear()
            self.formatComboBox.addItem("CSV")
            self.formatComboBox.setEnabled(False)
        else:
            self.converterLabel.setPixmap(self.csvPixmap)
            
            if self.outputEdit.text() != "":
                fileName = self.outputEdit.text().split(".")
                self.outputEdit.setText(str(fileName[0])+"."+self.converter.format)

            self.inputLabel.setText("Vstupný súbor (.csv) :")
            if self.converter.format == "ttl":
                self.outputLabel.setText("Výstupný súbor (.ttl) :")
            else:
                self.outputLabel.setText("Výstupný súbor (.xml) :")
            
            self.formatComboBox.clear()
            index = 0
            if self.converter.format == "xml":
                index = 1
            self.formatComboBox.addItems(["RDF/TTL", "RDF/XML"])
            self.formatComboBox.setCurrentIndex(index)
            self.formatComboBox.setEnabled(True)

    def convert(self):
        """
        Pomocná funkcia spúšťajúca konverziu.
        """

        if self.inputEdit.text() and self.outputEdit.text():
            if (self.reverseButton.isChecked()) :
                resultCode = self.converter.RDFtoCSV()
            else :
                resultCode = self.converter.CSVtoRDF()

            if resultCode == -1:
                self.errorLabel.setText("Chyba vstupného súboru")
                self.inputEdit.setStyleSheet("background: '#dba4a4'")
            elif resultCode == -2:
                self.errorLabel.setText("Chyba výstupného súboru")
                self.outputEdit.setStyleSheet("background: '#dba4a4'")
            elif resultCode == -3:
                self.errorLabel.setText("Chyba súboru metaúdajov")   

        elif self.inputEdit.text():
            self.errorLabel.setText("Výstupný súbor nebol špecifikovaný")
            self.outputEdit.setStyleSheet("background: '#dba4a4'")
        elif self.outputEdit.text():
            self.errorLabel.setText("Vstupný súbor nebol špecifikovaný")
            self.inputEdit.setStyleSheet("background: '#dba4a4'")
        else:
            self.errorLabel.setText("Vstupný ani výstupný súbor neboli špecifikované")
            self.inputEdit.setStyleSheet("background: '#dba4a4'")
            self.outputEdit.setStyleSheet("background: '#dba4a4'")