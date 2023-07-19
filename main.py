from PyQt6.QtWidgets import QApplication
import sys
from converter_interface import MainWindow

"""
    Hlavný spúšťací súbor aplikácie.
    Vytvorí nové okno "window" a zobrazí ho
"""

app = QApplication(sys.argv)
QApplication.setStyle('Fusion')
window = MainWindow()
window.show()
app.exec()
