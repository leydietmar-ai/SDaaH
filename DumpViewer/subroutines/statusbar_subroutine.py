import locale
from PySide6.QtWidgets import QLabel, QStatusBar
from PySide6.QtCore import Qt, QDate, QTime, QTimer
from PySide6.QtGui import QFont

locale.setlocale(locale.LC_ALL, "de")


def status_bar(self):
    # Statusbar erzeugen
    self.status_bar = QStatusBar()
    self.setStatusBar(self.status_bar)

    # Wochentage
    days = [
        "Montag", "Dienstag", "Mittwoch", "Donnerstag",
        "Freitag", "Samstag", "Sonntag"
    ]

    # Datum initial
    date = QDate.currentDate()
    currday = date.dayOfWeek() - 1

    # Label 1: Copyright
    #self.myLabel1.setTextFormat(Qt.RichText)
    self.myLabel1 = QLabel("© 2026 by SDaaH <sub>Dietmar Ley</sub> Software Development as a Hobby")
    self.status_bar.addPermanentWidget(self.myLabel1, 1)

    # Label 2: Datum + Uhrzeit (wird später aktualisiert)
    self.myLabel2 = QLabel()
    self.status_bar.addPermanentWidget(self.myLabel2, 0)
    
    self.statusBar().setObjectName("main_statusbar")

    # ---------------------------------------------------------
    # Timer für Live-Uhrzeit + Datum-Wechsel um Mitternacht
    # ---------------------------------------------------------
    self.current_date = date  # merken für Tageswechsel

    def update_time():
        now = QTime.currentTime()
        today = QDate.currentDate()

        # Datum hat gewechselt?
        if today != self.current_date:
            self.current_date = today
            # Wochentag neu berechnen
            new_day = today.dayOfWeek() - 1
            self.myLabel2.setText(
                f"Heute ist {days[new_day]}, der {today.toString('dd.MM.yyyy')}, "
                f"Uhrzeit: {now.toString('HH:mm:ss')}"
            )
        else:
            # Nur Uhrzeit aktualisieren
            self.myLabel2.setText(
                f"Heute ist {days[currday]}, der {today.toString('dd.MM.yyyy')}, "
                f"Uhrzeit: {now.toString('HH:mm:ss')}"
            )

    # Timer starten
    self.timer = QTimer()
    self.timer.timeout.connect(update_time)
    self.timer.start(1000)

    update_time()

