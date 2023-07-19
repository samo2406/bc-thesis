from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QPlainTextEdit
from PyQt6.QtGui import QIcon
from converter import Converter

class MetadataWindow(QWidget):
    """
    Trieda používateľského rozhrania čítania metaúdajov.
    """

    def __init__(self):
        """
        Inicializácia všetkých prvkov používateľského rozhrania aplikácie.
        """

        super().__init__()

        self.setWindowTitle("Metadáta")
       
        readMetadataButton = QPushButton("Výber súboru..")
        readMetadataButton.clicked.connect(self.readMetadataFileDialog)
        self.converter = Converter()
        readMetadataButton.setIcon(QIcon(self.converter.resource_path("folder.png")))
        metadataLabel = QLabel("Metadáta vybraného súboru :")
        self.fileLabel = QLabel("")
        self.metadataOutput = QPlainTextEdit()
        self.metadataOutput.setReadOnly(True)
        
        layout = QVBoxLayout()
        layout.addWidget(readMetadataButton)
        layout.addWidget(metadataLabel)
        layout.addWidget(self.metadataOutput)
        layout.addWidget(self.fileLabel)

        self.setLayout(layout)

        self.setStyleSheet("""
            QWidget {
                background-color: "#e8feff";
                font-size: 16px;
                color: "black";
            }
            QPlainTextEdit {
                background: #ffffff;
            }
            QPushButton {
                border-radius: 6px;
                font-size: 16px;
                padding: 6px 10px 6px 10px;
                margin: 5px;
                background: #abddff;
                border: 1px solid rgb(66, 184, 221);
                border-radius: 6px;
            }
            QPushButton:hover {
                background: #8dc0e3;
            }
        """)

    def readMetadataFileDialog(self):
        """
        Dialógové okno výberu súboru metaúdajov na prečítanie,
            automaticky spustí čítanie a zobrazí výsledok.
        """

        fileDialog = QFileDialog()
        fileDialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        fileDialog.setViewMode(QFileDialog.ViewMode.List)
        if fileDialog.exec():
            metadata = Converter.ReadMetadata(fileDialog.selectedFiles()[0])
            self.metadataOutput.setPlainText(''.join(metadata))
            self.fileLabel.setText(fileDialog.selectedFiles()[0])
            if (metadata == "Tento súbor neobsahuje metadáta."):
                size = self.metadataOutput.fontMetrics().boundingRect(metadata)
            else:
                size = self.metadataOutput.fontMetrics().boundingRect(max(metadata, key=len))
            self.setFixedWidth(int((size.width()*1.05)+30))
            self.setFixedHeight(int((len(metadata)+2)*size.height())+125)
